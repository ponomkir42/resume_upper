import pytest

import httpx
import respx

from config import config
from services.habr_request import refresh_habr_resume


@pytest.mark.asyncio
@respx.mock
async def test_refresh_habr_resume_success(caplog):
    route = respx.get(config.HABR_UPDATE_URL).mock(
        return_value=httpx.Response(status_code=200, json={"user": {"fullName": "Test User"}})
    )
    await refresh_habr_resume()

    assert route.called
    assert "Successfully refreshed habr resume for user: Test User" in caplog.text


@pytest.mark.asyncio
@respx.mock
async def test_refresh_habr_resume_bad_cookies(caplog):
    route = respx.get(config.HABR_UPDATE_URL).mock(
        return_value=httpx.Response(status_code=403)
    )
    tg_route = respx.post(f"{config.TG_API_URL}{config.TG_BOT_TOKEN}/sendMessage").mock(
        return_value=httpx.Response(status_code=200)
    )
    await refresh_habr_resume()

    assert route.called
    assert tg_route.called
    assert "HTTP error in refresh_habr_resume" in caplog.text


@pytest.mark.asyncio
@respx.mock
async def test_refresh_habr_resume_unexpected_response(caplog):
    route = respx.get(config.HABR_UPDATE_URL).mock(
        return_value=httpx.Response(status_code=200, json={"unexpected_key": {}})
    )
    tg_route = respx.post(f"{config.TG_API_URL}{config.TG_BOT_TOKEN}/sendMessage").mock(
        return_value=httpx.Response(status_code=200)
    )
    await refresh_habr_resume()

    assert route.called
    assert tg_route.called
    assert "Unexpected response" in caplog.text
