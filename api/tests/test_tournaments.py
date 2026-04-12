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

async def test_admin_can_create_tournament(client: AsyncClient, admin_user, tournament_data):
    h = await auth_header(client, "testadmin", "admin123")
    resp = await client.post("/tournaments/", json=tournament_data, headers=h)
    assert resp.status_code == 201
    assert resp.json()["name"] == "Major Copenhagen 2024"

async def test_team_registration_fails_if_less_than_5_players(client: AsyncClient, team_and_user, admin_user, tournament_data):
    h_admin = await auth_header(client, "testadmin", "admin123")
    t_resp = await client.post("/tournaments/", json=tournament_data, headers=h_admin)
    t_id = t_resp.json()["id"]

    h_team = await auth_header(client, "testteam", "team123")
    resp = await client.post(f"/tournaments/{t_id}/registrations", headers=h_team)
    
    assert resp.status_code == 400
    assert "barem 5 igrača" in resp.json()["message"]

async def test_registration_deadline_logic(client: AsyncClient, admin_user, team_and_user, db, tournament_data):
    h_admin = await auth_header(client, "testadmin", "admin123")
    t_resp = await client.post("/tournaments/", json=tournament_data, headers=h_admin)
    t_id = t_resp.json()["id"]

    from app.models.player import Player
    team, _ = team_and_user
    for i in range(5):
        p = Player(first_name=f"P{i}", last_name="T", nickname=f"n{i}", position="T", birth_date=date(2000,1,1), team_id=team.id)
        db.add(p)
    await db.commit()

    # 3. Testiraj OPEN fazu (unutar roka)
    with freeze_time(datetime.now(timezone.utc)):
        h_team = await auth_header(client, "testteam", "team123")
        resp = await client.post(f"/tournaments/{t_id}/registrations", headers=h_team)
        assert resp.status_code == 201

    # 4. Testiraj CLOSED fazu (prošao rok)
    with freeze_time(datetime.now(timezone.utc) + timedelta(days=25)):
        # Moramo re-login unutar freeze_time jer bi inače token iz prošlosti bio istekao
        h_team_future = await auth_header(client, "testteam", "team123")
        resp = await client.post(f"/tournaments/{t_id}/registrations", headers=h_team_future)
        assert resp.status_code == 400
        assert resp.json()["code"] == "deadline_passed"
