from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db

dashboard_router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@dashboard_router.get("/severity-counts")
async def get_open_issues_by_severity(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("""
        SELECT severity, COUNT(*) 
        FROM issues 
        WHERE status = 'open' 
        GROUP BY severity
    """))

    rows = result.fetchall()
    return [{"severity": row[0], "count": row[1]} for row in rows]
