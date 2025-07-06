import asyncio
import json
import pytest
from httpx import AsyncClient

from app.main import app
from app.database import AsyncSessionLocal, engine, Base
from app.models.user import RoleEnum

pytestmark = pytest.mark.anyio   # enable pytest-asyncio

@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    # create fresh schema in the same test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # nothing to tear down


async def register_user(client, email, role=RoleEnum.reporter):
    res = await client.post("/api/auth/register", json={
        "email": email,
        "password": "test1234",
        "role": role
    })
    assert res.status_code == 200, res.text
    return res.json()

async def login(client, email):
    res = await client.post("/api/auth/login", json={
        "email": email,
        "password": "test1234"
    })
    assert res.status_code == 200
    return res.json()["access_token"]

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# ─── TESTS ────────────────────────────────────────────────────────────────────

async def test_full_flow(client):
    # 1. register + login
    await register_user(client, "rep@example.com")
    token = await login(client, "rep@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # 2. submit issue
    res = await client.post(
        "/api/issues/",
        headers=headers,
        files={"file": ("dummy.txt", b"hello")},
        data={
            "title": "pytest issue",
            "description": "pytest desc",
            "severity": "LOW"
        }
    )
    assert res.status_code == 200
    issue_id = res.json()["id"]

    # 3. list issues (should contain our issue)
    res = await client.get("/api/issues/", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert any(i["id"] == issue_id for i in data)

    # 4. dashboard counts should show LOW ≥ 1
    res = await client.get("/api/dashboard/severity-counts", headers=headers)
    assert res.status_code == 200
    counts = {row["severity"]: row["count"] for row in res.json()}
    assert counts.get("LOW", 0) >= 1
