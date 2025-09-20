import typing
import datetime

import httpx

from . import schemas, errors

PRODUCT_NOT_FOUND_ERR_MSG = "Product with article '{article}' not found"

JsonType = dict[str, typing.Any]

class WBFeedbacksScrapper:
    """Wildberries feedback scrapper from internal api."""

    URLS = {
        "detail_v2": "https://card.wb.ru/cards/v2/detail",
        "feedbacks_v2": (
            "https://feedbacks{data_center}.wb.ru/feedbacks/v2/{root}"
        ),
    }
    _WB_DATA_CENTERS_AMOUNT = 2
    _DEFAULT_DEST_CSV = "-1257786,-59204,-58159,-115136"

    def __init__(
        self,
        *,
        article: int,
        client: httpx.Client,
        dest_csv: str = _DEFAULT_DEST_CSV,
        root: int | None = None,
    ):
        self._article = article
        self._client = client
        self._root = root
        if root is None:
            self._common_params = {
                "dest": dest_csv,
                "nm": article,
            }

    def _request(
        self,
        *,
        url: httpx.URL | str,
        params: httpx.QueryParams | None = None,
    ) -> JsonType:
        """Return response body from get request."""
        response = self._client.get(url=url, params=params)
        response.raise_for_status()
        return response.json()

    def _get_product_root(self) -> int:
        """Return product root and make request by article."""
        data = self._request(
            url=self.URLS["detail_v2"],
            params=self._common_params,
        )
        if not data["data"]["products"]:
            raise errors.ProductNotFound(
                PRODUCT_NOT_FOUND_ERR_MSG.format(
                    article=self._article,
                ),
            )
        return data["data"]["products"][0]["root"]

    def _normalize_feedbacks(self, data: JsonType) -> list[schemas.Feedback]:
        """Return list of feedback normalized schemas from response body."""
        return [schemas.Feedback(
            id=feedback["id"],
            username=feedback["wbUserDetails"]["name"],
            product_article=self._article,
            valuation=feedback["productValuation"],
            comment=feedback["text"],
            pros=feedback["pros"],
            cons=feedback["cons"],
            created_on_wb=feedback["createdDate"],
        ) for feedback in data["feedbacks"]]


    def _feedbacks_from_root(
        self,
        root: int,
    ) -> list[schemas.Feedback] | None:
        """Return list of Feedback schemas."""
        for data_center_id in range(1, self._WB_DATA_CENTERS_AMOUNT + 1):
            data = self._request(
                url=self.URLS["feedbacks_v2"].format(
                    data_center=data_center_id,
                    root=root,
                ),
            )
            if data["feedbacks"]:
                return self._normalize_feedbacks(data)
        return None

    def _feedbacks_from_article(self) -> list[schemas.Feedback] | None:
        """Return feedbacks by article."""
        return self._feedbacks_from_root(root=self._get_product_root())

    def _filter_feedbacks(
        self,
        *,
        feedbacks: list[schemas.Feedback],
        valuation: int,
        day_limit: int,
        ) -> list[schemas.Feedback]:
        """Return and filter Feedback schemas by conditions."""
        def filter_func(feedback: schemas.Feedback) -> bool:
            """Function for filtering feedbacks schemas."""
            timezone = datetime.timezone.utc
            start_date = datetime.datetime.now(
                timezone,
            ) - datetime.timedelta(
                days=day_limit,
            )
            return (
                feedback.created_on_wb >= start_date
            ) and (
                feedback.valuation <= valuation
            )
        return list(filter(filter_func, feedbacks))

    def get_feedbacks(
        self,
        valuation: int,
        day_limit: int,
    ) -> list[schemas.Feedback]:
        """Return filtered feedbacks of product."""
        if self._root is not None:
            # if scrapper have product root, searching feedbacks instantly
            feedbacks = self._feedbacks_from_root()
        if self._root is None:
            # otherwise get root first than request for feedbacks
            feedbacks = self._feedbacks_from_article()
        if not feedbacks:
            return None
        return self._filter_feedbacks(
            feedbacks=feedbacks,
            valuation=valuation,
            day_limit=day_limit,
        )
