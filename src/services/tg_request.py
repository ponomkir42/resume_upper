import httpx

from config import config, Status
from utils import logger


async def send_tg_message(text: str) -> None:
    if config.TG_STATUS == Status.DISABLED:
        return
    elif config.TG_STATUS == Status.LACK_OF_DATA:
        logger.warning("Please make sure that you pass Telegram bot token and chat id in .env file")
        return

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{config.TG_API_URL}{config.TG_BOT_TOKEN}/sendMessage",
                params={
                    "chat_id": config.TG_CHAT_ID,
                    "text": text
                }
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error in send_tg_message {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error(f"Unexpected error in send_tg_message {str(e)}")
