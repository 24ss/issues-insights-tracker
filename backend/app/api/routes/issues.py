from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import shutil, os

from app.database import get_db
from app.models.issue import Issue, StatusEnum
from app.models.user import User, RoleEnum
from app.schemas.issue import IssueUpdate, IssueRead
from app.api.deps import get_current_user

issues_router = APIRouter(prefix="/api/issues", tags=["issues"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@issues_router.post("/", response_model=IssueRead)
async def create_issue(
    title: str = Form(...),
    description: str = Form(""),
    severity: str = Form(...),
    file: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    filename = None
    if file:
        filename = os.path.join(UPLOAD_DIR, file.filename)
        with open(filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    issue = Issue(
        title=title,
        description=description,
        severity=severity,
        attachment=file.filename if file else None,
        reporter_id=user.id
    )
    db.add(issue)
    await db.commit()
    await db.refresh(issue)
    # Notify SSE subscribers
    for subscriber in subscribers:
        await subscriber.put(f"Issue {issue.id} created")

    return issue


@issues_router.get("/", response_model=List[IssueRead])
async def get_issues(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    stmt = select(Issue)
    if user.role == RoleEnum.reporter:
        stmt = stmt.where(Issue.reporter_id == user.id)
    result = await db.execute(stmt)
    return result.scalars().all()


@issues_router.get("/{issue_id}", response_model=IssueRead)
async def get_issue(issue_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Issue).where(Issue.id == issue_id))
    issue = result.scalar_one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    if user.role == RoleEnum.reporter and issue.reporter_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return issue


@issues_router.put("/{issue_id}", response_model=IssueRead)
async def update_issue(issue_id: int, issue_in: IssueUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Issue).where(Issue.id == issue_id))
    issue = result.scalar_one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Role checks
    if user.role == RoleEnum.reporter and issue.reporter_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    if user.role == RoleEnum.maintainer and issue_in.status is None:
        raise HTTPException(status_code=403, detail="Maintainer can only triage/update status")

    for field, value in issue_in.dict(exclude_unset=True).items():
        setattr(issue, field, value)

    await db.commit()
    await db.refresh(issue)
     # Notify SSE subscribers
    for subscriber in subscribers:
        await subscriber.put(f"Issue {issue.id} updated")

    return issue


@issues_router.delete("/{issue_id}")
async def delete_issue(issue_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Issue).where(Issue.id == issue_id))
    issue = result.scalar_one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    if user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admin can delete issues")

    await db.delete(issue)
    await db.commit()
    return {"msg": "Issue deleted"}

from fastapi.responses import StreamingResponse
import asyncio

subscribers: list[asyncio.Queue] = []

@issues_router.get("/stream")
async def issue_event_stream():
    queue = asyncio.Queue()
    subscribers.append(queue)

    async def event_generator():
        try:
            while True:
                data = await queue.get()
                yield f"data: {data}\n\n"
        except asyncio.CancelledError:
            subscribers.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")