from datetime import date

from sqlalchemy import Column, Date, Integer, String, UniqueConstraint

from app.database import Base


class DailyStats(Base):
    __tablename__ = "daily_stats"

    id     = Column(Integer, primary_key=True)
    day    = Column(Date, default=date.today, index=True)
    status = Column(String, nullable=False)
    count  = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("day", "status", name="uq_day_status"),
    )
