import datetime

import pydantic

class Feedback(pydantic.BaseModel):
    """Feedback validation schema."""

    id: str
    username: str
    product_article: int
    valuation: int
    comment: str | None = None
    pros: str | None = None
    cons: str | None = None
    created_on_wb: datetime.datetime
