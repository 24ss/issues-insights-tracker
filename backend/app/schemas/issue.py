from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class SeverityEnum(str, Enum):
    low = "LOW"
    medium = "MEDIUM"
    high = "HIGH"
    critical = "CRITICAL"

class StatusEnum(str, Enum):
    open = "OPEN"
    triaged = "TRIAGED"
    in_progress = "IN_PROGRESS"
    done = "DONE"

class IssueCreate(BaseModel):
    title: str
    description: Optional[str] = None
    severity: SeverityEnum
    attachment: Optional[str] = None  # For now, just store filename/path

class IssueUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    severity: Optional[SeverityEnum]
    status: Optional[StatusEnum]
    assigned_to_id: Optional[int]
    attachment: Optional[str] = None

class IssueRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    severity: SeverityEnum
    status: StatusEnum
    attachment: Optional[str]
    reporter_id: int
    assigned_to_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
