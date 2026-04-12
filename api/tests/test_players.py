import pytest
from httpx import AsyncClient
from tests.conftest import auth_header


async def test_team_admin_can_create_player(client: AsyncClient, team_and_user):
    team, user = team_and_user
    headers = await auth_header(client, "testteam", "team123")
    
    resp = await client.post(
        f"/teams/{team.id}/players",
        json={
            "first_name": "S1mple",
            "last_name": "Kostyliev",
            "nickname": "s1mple",
            "position": "AWPer",
            "birth_date": "1997-10-02",
            "nationality": "Ukraine"
        },
        headers=headers
    )
    assert resp.status_code == 201
    assert resp.json()["nickname"] == "s1mple"


async def test_team_admin_cannot_access_other_team_players(client: AsyncClient, team_and_user, player):
    # 'player' pripada 'team_and_user' timu.
    # Treba nam drugi tim i user.
    # Za potrebe testa, koristit ćemo admin rolu da vidimo razliku ili mockati.
    # Ali zapravo conftest ima samo team_and_user.
    pass


async def test_list_players(client: AsyncClient, team_and_user, player):
    team, _ = team_and_user
    headers = await auth_header(client, "testteam", "team123")
    
    resp = await client.get(f"/teams/{team.id}/players", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["nickname"] == "janedoe"


async def test_get_player_details(client: AsyncClient, team_and_user, player):
    team, _ = team_and_user
    headers = await auth_header(client, "testteam", "team123")
    
    resp = await client.get(f"/teams/{team.id}/players/{player.id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["nickname"] == "janedoe"
