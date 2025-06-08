from enum import Enum

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Status(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    LACK_OF_DATA = "lack_of_data"


class CronSettings(BaseSettings):
    hour: int
    minute: int = 0


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", env_file_encoding="utf-8"
    )
    SERVICE_NAME: str = "hh_upper"

    LOGS_PATH: str = "/runtime/logs"
    SERVICE_CONTEXT: str = "local"

    # telegram
    TG_STATUS: Status = Status.ENABLED
    TG_BOT_TOKEN: str | None = None
    TG_CHAT_ID: str | None = None
    TG_API_URL: str = "https://api.telegram.org/bot"

    # headhunter
    HH_STATUS: Status = Status.ENABLED
    HH_XSRF_TOKEN: str | None = None
    HH_TOKEN: str | None = None
    HH_UID: str | None = None
    HH_RESUME_ID: str | None = None
    HH_CRON_SETTINGS: list[CronSettings] = [
        CronSettings(hour=7),
        CronSettings(hour=11, minute=5),
        CronSettings(hour=15, minute=10),
        CronSettings(hour=19, minute=15),
        CronSettings(hour=23, minute=20)
    ]
    HH_UPDATE_URL: str = "https://hh.ru/applicant/resumes/touch"

    # habr
    HABR_STATUS: Status = Status.ENABLED
    HABR_UUID: str | None = None
    HABR_USER_TOKEN: str | None = None
    HABR_CRON_SETTINGS: list[CronSettings] = [
        CronSettings(hour=10),
    ]
    HABR_UPDATE_URL: str = "https://career.habr.com/api/frontend_v1/users/me"

    @model_validator(mode="after")
    def validate_config(self) -> "Config":
        # Telegram
        if self.TG_STATUS == Status.ENABLED and not (self.TG_BOT_TOKEN and self.TG_CHAT_ID):
            self.TG_STATUS = Status.LACK_OF_DATA

        # HeadHunter
        if self.HH_STATUS == Status.ENABLED and not all([
            self.HH_XSRF_TOKEN,
            self.HH_TOKEN,
            self.HH_UID,
            self.HH_RESUME_ID
        ]):
            self.HH_STATUS = Status.LACK_OF_DATA

        # Habr
        if self.HABR_STATUS == Status.ENABLED and not all([
            self.HABR_UUID,
            self.HABR_USER_TOKEN
        ]):
            self.HABR_STATUS = Status.LACK_OF_DATA
        return self

config = Config()
