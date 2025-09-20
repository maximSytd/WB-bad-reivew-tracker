from tortoise import fields


class TimeStampMixin:
    """Model timestamp mixin with created and modified fields."""

    created = fields.DatetimeField(
        auto_now_add=True,
    )
    modified = fields.DatetimeField(
        auto_now=True,
    )
