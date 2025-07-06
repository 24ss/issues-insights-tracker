from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User, RoleEnum
from app.schemas.user import UserCreate, UserRead 
from app.schemas.auth import LoginRequest
from app.schemas.token import Token
from app.core.security import hash_password, verify_password, create_access_token
from app.config import get_settings

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])

@auth_router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=user_in.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@auth_router.post("/login", response_model=Token)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# ─── GOOGLE OAUTH LOGIN ──────────────────────────────────────────────────────────
from pydantic import BaseModel
import httpx

class GoogleLoginRequest(BaseModel):
    id_token: str

GOOGLE_CLIENT_ID = get_settings().dict().get("GOOGLE_CLIENT_ID")  # set in .env

@auth_router.post("/google-login", response_model=Token)
async def google_login(payload: GoogleLoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Accept Google ID-token from frontend, verify with Google, and
    return our own JWT if email is valid.
    """
    # Verify token with Google
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": payload.id_token},
            timeout=5,
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    info = resp.json()
    if info.get("aud") != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Wrong Google client ID")

    email = info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email not found in token")

    # user-upsert
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar()
    if not user:
        user = User(email=email, role=RoleEnum.reporter, hashed_password="")  # pw blank
        db.add(user)
        await db.commit()
        await db.refresh(user)

    jwt_token = create_access_token({"sub": str(user.id)})
    return {"access_token": jwt_token, "token_type": "bearer"}
