from fastapi import APIRouter
from app.api.routes import auth, issues, dashboard

api_router = APIRouter()
api_router.include_router(auth.auth_router)
api_router.include_router(issues.issues_router)
api_router.include_router(dashboard.dashboard_router)
