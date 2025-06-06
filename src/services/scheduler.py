from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import config, Status
from services.habr_request import refresh_habr_resume
from services.hh_request import refresh_hh_resume
from utils import logger


def configure_hh_jobs(scheduler: AsyncIOScheduler) -> None:
    if config.HH_STATUS == Status.ENABLED:
        for job in config.HH_CRON_SETTINGS:
            scheduler.add_job(refresh_hh_resume, trigger="cron", **job.model_dump())
    elif config.HH_STATUS == Status.LACK_OF_DATA:
        logger.warning("Please make sure that you pass Headhunter cookies in .env file")

def configure_habr_jobs(scheduler: AsyncIOScheduler) -> None:
    if config.HABR_STATUS == Status.ENABLED:
        for job in config.HABR_CRON_SETTINGS:
            scheduler.add_job(refresh_habr_resume, trigger="cron", **job.model_dump())
    elif config.HABR_STATUS == Status.LACK_OF_DATA:
        logger.warning("Please make sure that you pass Habr career cookies in .env file")

async def setup_scheduler() -> AsyncIOScheduler:
    scheduler  = AsyncIOScheduler()
    configure_hh_jobs(scheduler)
    configure_habr_jobs(scheduler)
    return scheduler
