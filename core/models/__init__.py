from tortoise import models, fields


class TimeStampMixin:
    """Model timestamp mixin with created and modified fields."""

    created = fields.DatetimeField(
        auto_now_add=True,
    )
    modified = fields.DatetimeField(
        auto_now=True,
    )

class BaseModel(TimeStampMixin, models.Model):
    """Base db model with integer id and timestamp mixin."""

    id = fields.IntField(
        primary_key=True,
    )

    class Meta:
        abstract = True
