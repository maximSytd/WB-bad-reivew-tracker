import typing
import contextlib

import httpx
import httpx_retries
import tortoise

from core.config import tortoise_settings

REQUEST_TIMEOUT_SEC = 3
MAX_RETRIES = 3
RETRY_BACKOFF = 0.5

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
    config: dict[str, typing.Any] = tortoise_settings,
) -> typing.AsyncGenerator[None, None]:
    """Yield None and manage tortoise db connection."""
    await tortoise.Tortoise.init(config=config)
    try:
        yield
    finally:
        await tortoise.Tortoise.close_connections()

def common_headers() -> dict[str, str | tuple[str, ...]]:
    """Return common headers for http client."""
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
