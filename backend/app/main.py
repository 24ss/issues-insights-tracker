from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api import api_router

app = FastAPI(
    title="Issues & Insights Tracker",
    description="Submit, triage, and track issues with real-time updates and analytics.",
    version="1.0.0",
    contact={
        "name": "Support Team",
        "email": "support@example.com"
    },
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Router
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Issues & Insights Tracker API"}

# 🔐 Custom OpenAPI schema to support Bearer token auth in Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
