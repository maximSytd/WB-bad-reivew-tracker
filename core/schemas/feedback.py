import typing
import datetime

import pydantic

from .. import models


VALUATION_VAL_MSG = "Valuation should be between 1 and 5"
PRODUCT_ARTICLE_VAL_MSG = (
    "Article should contains less than "
    f"{models.Feedback.PRODUCT_ARTICLE_MAX_DIGITS + 1} digits"
)

def validate_valuation(value: int) -> int:
    """Return bool and validate valuation field."""
    if value < 1 or value > 5:
        raise pydantic.ValidationError(VALUATION_VAL_MSG)
    return value

def validate_product_article(value: int) -> int:
    """Return bool and validate product_article field."""
    if len(str(value)) > models.Feedback.PRODUCT_ARTICLE_MAX_DIGITS:
        raise pydantic.ValidationError(VALUATION_VAL_MSG)
    return value

class Feedback(pydantic.BaseModel):
    """Feedback validation schema."""

    id: str = pydantic.Field(
        max_length=models.Feedback.ID_MAX_LEN,
    )
    username: str = pydantic.Field(
        max_length=models.Feedback.USERNAME_MAX_LEN,
    )
    product_article: typing.Annotated[
        int,
        pydantic.AfterValidator(
            validate_product_article,
        )
    ]
    valuation: typing.Annotated[
        int,
        pydantic.AfterValidator(
            validate_valuation,
        ),
    ]
    comment: str | None = pydantic.Field(
        default=None,
        max_length=models.Feedback.COMMENT_MAX_LEN,
    )
    pros: str | None = pydantic.Field(
        default=None,
        max_length=models.Feedback.PROS_MAX_LEN,
    )
    cons: str | None = pydantic.Field(
        default=None,
        max_length=models.Feedback.CONS_MAX_LEN,
    )
    created_on_wb: datetime.datetime
