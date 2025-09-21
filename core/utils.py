import typing
import contextlib

import httpx
import httpx_retries
import tortoise
import tabulate

from . import config, schemas

REQUEST_TIMEOUT_SEC = 3
MAX_RETRIES = 3
RETRY_BACKOFF = 0.5

TABULATION_MAX_FIELD_LEN = 25

ClientManagerType = typing.Generator[httpx.Client, None]

@contextlib.contextmanager
def client_manager(**kw) -> ClientManagerType:
    """Yield httpx client."""
    transport = httpx_retries.RetryTransport(
        retry=httpx_retries.Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_BACKOFF,
        ),
    )
    with httpx.Client(
        transport=transport,
        timeout=REQUEST_TIMEOUT_SEC,
        **kw,
    ) as c:
        yield c

@contextlib.asynccontextmanager
async def tortoise_context_manager(
    config: dict[str, typing.Any] = config.tortoise_settings,
) -> typing.AsyncGenerator[None, None]:
    """Yield None and manage tortoise db connection."""
    await tortoise.Tortoise.init(config=config)
    try:
        yield
    finally:
        await tortoise.Tortoise.close_connections()

def common_headers() -> dict[str, str | tuple[str, ...]]:
    """Return common headers for http client to work with wb api."""
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-ru,ru;q=0.9,en;q=0.8",
        "Referer": "https://www.wildberries.ru/",
        "Origin": "https://www.wildberries.ru",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Connection": "keep-alive",
    }


def shorten(value: typing.Any, max_len: int) -> str:
    """Return shorten to `max_len` size string."""
    end = "..."
    if not value:
        return "-"
    s = str(value)
    return s if len(s) <= max_len else s[: max_len - (len(end))] + end


def feedbacks_to_table(
    feedbacks: list[schemas.Feedback],
    max_len=TABULATION_MAX_FIELD_LEN,
) -> str:
    """Return tabulated string of feedbacks."""
    rows = []
    for f in feedbacks:
        row = {
            k: shorten(v, max_len=max_len)
            for k, v in f.model_dump(exclude="product_article").items()
        }
        rows.append(row)
    return tabulate.tabulate(rows, headers="keys", tablefmt="fancy_grid")
