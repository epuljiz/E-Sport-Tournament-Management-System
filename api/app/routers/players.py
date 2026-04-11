from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db, require_role
from app.models.user import User
from app.schemas.player import PlayerCreate, PlayerResponse, PlayerUpdate
from app.services import player_service

router = APIRouter()

@router.get("/{team_id}/players", response_model=list[PlayerResponse])
async def list_players(
    team_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "team_admin")),
):
    """Lista igrača za određeni tim uz provjeru prava pristupa."""
    return await player_service.list_players(db, team_id, user)

@router.post("/{team_id}/players", response_model=PlayerResponse, status_code=201)
async def create_player(
    team_id: int,
    body: PlayerCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "team_admin")),
):
    """Kreiranje novog igrača unutar tima."""
    return await player_service.create_player(db, team_id, body, user)

@router.get("/{team_id}/players/{player_id}", response_model=PlayerResponse)
async def get_player(
    team_id: int,
    player_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "team_admin")),
):
    """Dohvaćanje detalja igrača."""
    return await player_service.get_player(db, team_id, player_id, user)

@router.patch("/{team_id}/players/{player_id}", response_model=PlayerResponse)
async def update_player(
    team_id: int,
    player_id: int,
    body: PlayerUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "team_admin")),
):
    """Ažuriranje podataka igrača."""
    return await player_service.update_player(db, team_id, player_id, body, user)

@router.delete("/{team_id}/players/{player_id}", status_code=204)
async def delete_player(
    team_id: int,
    player_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "team_admin")),
):
    """Brisanje igrača."""
    await player_service.delete_player(db, team_id, player_id, user)
