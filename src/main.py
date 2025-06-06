import asyncio

from services.scheduler import setup_scheduler


async def main():
    scheduler = await setup_scheduler()
    scheduler.start()
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
