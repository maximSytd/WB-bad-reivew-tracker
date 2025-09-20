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
