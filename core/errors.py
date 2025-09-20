class BaseWbScrapperError(Exception):
    """Base exception for wb scrapper exceptions."""


class ProductNotFound(BaseWbScrapperError):
    """Product not found exception."""
