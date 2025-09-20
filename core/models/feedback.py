from tortoise import fields, models
from tortoise.validators import (
    MinValueValidator,
    MaxValueValidator,
    MaxLengthValidator,
)

from .base import TimeStampMixin


class Feedback(models.Model, TimeStampMixin):
    """Represent Feedback db model."""

    ID_MAX_LEN = 20
    USERNAME_MAX_LEN = 50
    PRODUCT_ARTICLE_MAX_DIGITS = 20
    VALUATION_MIN_VAL = 1
    VALUATION_MAX_VAL = 5
    COMMENT_MAX_LEN = 5000
    PROS_MAX_LEN = 2500
    CONS_MAX_LEN = 2500

    id = fields.CharField(
        primary_key=True,
        max_length=ID_MAX_LEN,
        validators=[
            MaxLengthValidator(ID_MAX_LEN),
        ],
    )
    username = fields.CharField(
        max_length=USERNAME_MAX_LEN,
        validators=[
            MaxLengthValidator(USERNAME_MAX_LEN),
        ],
    )
    product_article = fields.IntField()
    valuation = fields.IntField(
        validators=[
            MinValueValidator(VALUATION_MIN_VAL),
            MaxValueValidator(VALUATION_MAX_VAL),
        ],
    )
    comment = fields.TextField(
        max_length=COMMENT_MAX_LEN,
        null=True,
        validators=[
            MaxLengthValidator(COMMENT_MAX_LEN),
        ],
    )
    pros = fields.TextField(
        max_length=PROS_MAX_LEN,
        null=True,
        validators=[
            MaxLengthValidator(PROS_MAX_LEN),
        ],
    )
    cons = fields.TextField(
        max_length=CONS_MAX_LEN,
        null=True,
        validators=[
            MaxLengthValidator(CONS_MAX_LEN),
        ],
    )
    created_on_wb = fields.DatetimeField()
