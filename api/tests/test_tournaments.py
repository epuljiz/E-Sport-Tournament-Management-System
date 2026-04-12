import pytest
from datetime import datetime, date, timedelta, timezone
from httpx import AsyncClient
from freezegun import freeze_time
from tests.conftest import auth_header

@pytest.fixture
async def tournament_data():
    now = datetime.now(timezone.utc)
    return {
        "name": "Major Copenhagen 2024",
        "game": "Counter-Strike 2",
        "start_date": str(date.today() + timedelta(days=30)),
        "location": "Copenhagen, Denmark",
        "prelim_deadline": (now + timedelta(days=10)).isoformat(),
        "final_deadline": (now + timedelta(days=20)).isoformat()
    }

@pytest.mark.asyncio
async def test_admin_can_create_tournament(client: AsyncClient, admin_user, tournament_data):
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.post("/tournaments/", json=tournament_data, headers=headers)
    assert resp.status_code == 201
    assert resp.json()["name"] == "Major Copenhagen 2024"

@pytest.mark.asyncio
async def test_team_registration_fails_if_less_than_5_players(client: AsyncClient, team_and_user, admin_user, tournament_data):
    # Tim u conftestu ima samo jednog usera (ali tim_and_user fixture ne dodaje 5 igrača)
    headers_admin = await auth_header(client, "testadmin", "admin123")
    t_resp = await client.post("/tournaments/", json=tournament_data, headers_admin=headers_admin)
    t_id = t_resp.json()["id"]

    headers_team = await auth_header(client, "testteam", "team123")
    resp = await client.post(f"/tournaments/{t_id}/registrations", headers=headers_team)
    
    assert resp.status_code == 400
    assert "barem 5 igrača" in resp.json()["detail"]

@pytest.mark.asyncio
async def test_registration_deadline_logic(client: AsyncClient, admin_user, team_and_user, db, tournament_data):
    # 1. Kreiraj turnir
    headers_admin = await auth_header(client, "testadmin", "admin123")
    t_resp = await client.post("/tournaments/", json=tournament_data, headers=headers_admin)
    t_id = t_resp.json()["id"]

    # 2. Dodaj 5 igrača timu (id tima iz conftesta je dostupan preko team_and_user)
    from app.models.player import Player
    team, _ = team_and_user
    for i in range(5):
        p = Player(first_name=f"P{i}", last_name="Test", nickname=f"nick{i}", position="Test", birth_date=date(2000,1,1), team_id=team.id)
        db.add(p)
    await db.commit()

    # 3. Testiraj OPEN fazu (unutar roka)
    headers_team = await auth_header(client, "testteam", "team123")
    with freeze_time(datetime.now(timezone.utc)):
        resp = await client.post(f"/tournaments/{t_id}/registrations", headers=headers_team)
        assert resp.status_code == 201

    # 4. Testiraj CLOSED fazu (prošao rok)
    with freeze_time(datetime.now(timezone.utc) + timedelta(days=25)):
        resp = await client.post(f"/tournaments/{t_id}/registrations", headers=headers_team)
        assert resp.status_code == 400
        assert resp.json()["code"] == "deadline_passed"
