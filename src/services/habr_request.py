import httpx

from config import config
from utils import logger, handle_request_error


cookies = {
    "habr_uuid": config.HABR_UUID,
    "_career_session": config.HABR_CAREER_SESSION,
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "referer": "https://career.habr.com/",
    "cache-control": "max-age=0",
    "dnt": "1",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}


async def refresh_habr_resume() -> None:
    async with httpx.AsyncClient(cookies=cookies, headers=headers) as client:
        try:
            response = await client.get(config.HABR_UPDATE_URL)
            response.raise_for_status()
            result = response.json()
            if user := result.get("user"):
                logger.debug(f"Successfully refreshed habr resume for user: {user.get('fullName')}")
            else:
                raise Exception(f"Unexpected response: {result}")
        except Exception as e:
            await handle_request_error("refresh_habr_resume", e)
