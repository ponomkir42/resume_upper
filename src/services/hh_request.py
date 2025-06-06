import httpx

from config import config
from utils import logger, handle_request_error


form_data = {
    "resume": config.HH_RESUME_ID,
    "undirectable": "true"
}

cookies = {
    "hhtoken": config.HH_TOKEN,
    "hhuid": config.HH_UID,
    "cookie_policy_agreement": "true",
    "hhrole": "applicant",
}

headers = {
    "accept": "application/json",
    "accept-language": "ru,en-GB;q=0.9,en;q=0.8,en-US;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "cache-control": "max-age=0",
    "dnt": "1",
    "priority": "u=0, i",
    "referer": "https://hh.ru/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "x-xsrftoken": config.HH_XSRF_TOKEN,
}


async def refresh_hh_resume() -> None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://chelyabinsk.hh.ru/applicant/resumes/touch",
                data=form_data,
                cookies=cookies,
                headers=headers
            )
            response.raise_for_status()
        except Exception as e:
            await handle_request_error("refresh_hh_resume", e)
