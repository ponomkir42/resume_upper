import pytest

import httpx
import respx

from config import config
from services.hh_request import refresh_hh_resume


@respx.mock
@pytest.mark.asyncio
async def test_refresh_hh_resume_success(caplog):
    route = respx.post(config.HH_UPDATE_URL).mock(
        return_value=httpx.Response(status_code=200, text="<?xml version='1.0' encoding='utf-8'?><doc></doc>")
    )
    await refresh_hh_resume()

    assert route.called
    assert f"Successfully refreshed hh resume with id {config.HH_RESUME_ID}" in caplog.text


@respx.mock
@pytest.mark.asyncio
async def test_refresh_hh_resume_bad_cookies(caplog):
    # интересная особенность ответов на hh.ru - при 200 статуса возвращают xml-заглушку,
    # а при 403 статусе возвращают json
    route = respx.post(config.HH_UPDATE_URL).mock(
        return_value=httpx.Response(
            status_code=403,
            json={"anonymousUserType": "applicant", "errorCode": 403}
        )
    )
    tg_route = respx.post(f"{config.TG_API_URL}{config.TG_BOT_TOKEN}/sendMessage").mock(
        return_value=httpx.Response(status_code=200)
    )
    await refresh_hh_resume()

    assert route.called
    assert tg_route.called
    assert "HTTP error in refresh_hh_resume" in caplog.text
