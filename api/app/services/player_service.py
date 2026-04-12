from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import AppError
from app.models.player import Player
from app.models.user import User
from app.repositories import player_repo
from app.schemas.player import PlayerCreate, PlayerUpdate

def _check_team_access(current_user: User, team_id: int) -> None:
    """Voditelj tima smije upravljati samo igračima svog tima."""
    if current_user.role == "team_admin" and current_user.team_id != team_id:
        raise AppError("forbidden", "Ne možete pristupiti igračima drugog tima", 403)

async def list_players(
    db: AsyncSession,
    team_id: int,
    current_user: User,
    limit: int = 20,
    offset: int = 0,
) -> list[Player]:
    """Lista igrača tima s ownership provjerom."""
    _check_team_access(current_user, team_id)
    return await player_repo.get_by_team(db, team_id, limit=limit, offset=offset)

async def get_player(
    db: AsyncSession, team_id: int, player_id: int, current_user: User,
) -> Player:
    """Dohvati igrača s ownership provjerom."""
    _check_team_access(current_user, team_id)
    player = await player_repo.get_by_id(db, player_id)
    if not player or player.team_id != team_id:
        raise AppError("not_found", "Igrač nije pronađen", 404)
    return player

async def create_player(
    db: AsyncSession, team_id: int, body: PlayerCreate, current_user: User,
) -> Player:
    """Kreiraj igrača s ownership provjerom."""
    _check_team_access(current_user, team_id)
    player = Player(
        first_name=body.first_name,
        last_name=body.last_name,
        nickname=body.nickname,
        position=body.position,
        birth_date=body.birth_date,
        nationality=body.nationality,
        team_id=team_id,
    )
    return await player_repo.create(db, player)

async def update_player(
    db: AsyncSession, team_id: int, player_id: int,
    body: PlayerUpdate, current_user: User,
) -> Player:
    """Ažuriraj igrača s ownership provjerom."""
    player = await get_player(db, team_id, player_id, current_user)
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(player, field, value)
    await db.flush()
    return player

async def delete_player(
    db: AsyncSession, team_id: int, player_id: int, current_user: User,
) -> None:
    """Obriši igrača s ownership provjerom."""
    player = await get_player(db, team_id, player_id, current_user)
    await player_repo.delete(db, player)
