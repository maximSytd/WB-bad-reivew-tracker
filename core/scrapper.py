import typing
import datetime

import httpx

from . import schemas

JsonTypes = dict[str, typing.Any]

class WBFeedbacksScrapper:

    URLS = {
        "detail_v2": "https://card.wb.ru/cards/v2/detail",
        "feedbacks_v2": "https://feedbacks2.wb.ru/feedbacks/v2/{root}",
    }
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
        if not root:
            self._common_params = {
                "dest": dest_csv,
                "nm": article,
            }

    def _request(
        self,
        *,
        url: httpx.URL | str,
        params: httpx.QueryParams,
    ) -> JsonTypes:
        """Return response body from get request by `_client`. """
        response = self._client.get(url=url, params=params)
        return response.json()

    def _get_product_root(self) -> int:
        product = self._request(
            url=self.URLS["detail_v2"],
            params=self._common_params(),
        )
        root = ...
        return root

    def _feedbacks_from_root(
        self,
        root: int,
    ) -> list[schemas.Feedback] | None:
        return

    def _feedbacks_from_article(
        self,
        article: int,
    ) -> list[schemas.Feedback] | None:
        return

    def _filter_feedbacks(
            *,
            day_limit: int,
            feedbacks: list[schemas.Feedback],
        ) -> list[schemas.Feedback]:
        start_date = datetime.datetime.now() - datetime.timedelta(
            days=day_limit,
        )
        return list(
            filter(
                function=lambda feedback: feedback.created_on_wb >= start_date,
                iterable=feedbacks,
            ),
        )

    def get_feedbacks(self, day_limit: int = 3) -> list[schemas.Feedback]:
        if self._root is not None:
            feedbacks = self._feedbacks_from_root(self._root)
        if not feedbacks:
            feedbacks = self._feedbacks_from_article(self._article)
        if not feedbacks:
            return None
        return self._filter_feedbacks(feedbacks=feedbacks, day_limit=day_limit)