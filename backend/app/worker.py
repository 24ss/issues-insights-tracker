import asyncio
from datetime import date

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.issue import Issue
from app.models.daily_stats import DailyStats


async def collect_daily_stats() -> None:
    """
    Aggregate issue counts by status and upsert into daily_stats table.
    Runs every 30 minutes.
    """
    async with AsyncSessionLocal() as db:          # type: AsyncSession
        result = await db.execute(
            select(Issue.status, func.count())
            .group_by(Issue.status)
        )
        today = date.today()

        for status, count in result.all():
            # upsert (day, status) → count
            existing = await db.execute(
                select(DailyStats).where(
                    DailyStats.day == today,
                    DailyStats.status == status,
                )
            )
            row = existing.scalar_one_or_none()

            if row:
                row.count = count
            else:
                db.add(DailyStats(day=today, status=status, count=count))

        await db.commit()
        print(f"[worker] daily_stats updated {today}")


async def main() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(collect_daily_stats, "interval", minutes=30)
    scheduler.start()

    print("[worker] scheduler started (interval = 30 min)")
    while True:                # keep the process alive
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
