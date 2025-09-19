from tortoise import fields

from .base import BaseModel


class Feedback(BaseModel):
    id = fields.CharField(
        primary_key=True,
    )
    user_name = fields.CharField(
        ...,
    )
    product_article = fields.IntField(
        ...,
    )
    product_root = fields.IntField(
        ...,
    )
    product_valuation = fields.IntField(
        ...,
    )
    comment = fields.TextField(
        max_length=5000,
        null=True,
    )
