from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class SeverityEnum(str, enum.Enum):
    low = "LOW"
    medium = "MEDIUM"
    high = "HIGH"
    critical = "CRITICAL"

class StatusEnum(str, enum.Enum):
    open = "OPEN"
    triaged = "TRIAGED"
    in_progress = "IN_PROGRESS"
    done = "DONE"

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(Enum(SeverityEnum), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.open, nullable=False)
    attachment = Column(String, nullable=True)

    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    reporter = relationship("User", foreign_keys=[reporter_id])
    assignee = relationship("User", foreign_keys=[assigned_to_id])

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
