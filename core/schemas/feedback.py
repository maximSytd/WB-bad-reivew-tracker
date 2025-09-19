import datetime

import pydantic


class Feedback(pydantic.BaseModel):
    id: str
    user_name: str
    product_article: int
    product_root: int
    product_valuation: int
    comment: str | None = None
    pros: str | None = None # Достоинства
    cons: str | None = None # Недостатки
    created_on_wb: datetime.datetime
    updated_on_wb: datetime.datetime
