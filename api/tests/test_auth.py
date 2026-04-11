import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.conftest import auth_header

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, team_and_user):
    _, user = team_and_user
    resp = await client.post(
        "/auth/login",
        json={"username": "testteam", "password": "team123"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, team_and_user):
    resp = await client.post(
        "/auth/login",
        json={"username": "testteam", "password": "wrongpassword"}
    )
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_get_me_success(client: AsyncClient, team_and_user):
    _, user = team_and_user
    headers = await auth_header(client, "testteam", "team123")
    
    resp = await client.get("/auth/me", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "testteam"
    assert data["team_id"] is not None

@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    resp = await client.get("/auth/me")
    assert resp.status_code == 401
