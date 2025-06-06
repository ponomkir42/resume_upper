import httpx

from services.tg_request import send_tg_message
from utils import logger


async def handle_request_error(prefix: str, e: Exception):
    if isinstance(e, httpx.HTTPStatusError):
        message = f"HTTP error in {prefix}: {e.response.status_code} - {e.response.text}"
    else:
        message = f"Unexpected error in {prefix}: {str(e)}"
    logger.error(message)
    await send_tg_message(message[:200])
