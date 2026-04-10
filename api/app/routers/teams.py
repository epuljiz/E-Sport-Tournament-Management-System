from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db, require_role
from app.models.user import User
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate
from app.services import team_service

router = APIRouter()

@router.post("/", response_model=TeamResponse, status_code=201)
async def create_team(
    body: TeamCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    """Admin kreira novi esport tim."""
    team, user = await team_service.create_team(db, body.name, body.password, body.organization_name)
    # Mapiramo username admina za klijenta
    resp = TeamResponse.model_validate(team)
    resp.admin_username = user.username
    return resp

@router.get("/", response_model=list[TeamResponse])
async def list_teams(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "team_admin")),
):
    """Admin vidi sve, a team_admin vidi samo svoj tim."""
    teams = await team_service.list_teams(db, user)
    return [TeamResponse.model_validate(t) for t in teams]

@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "team_admin")),
):
    """Dohvaćanje detalja tima."""
    team = await team_service.get_team(db, team_id, user)
    return TeamResponse.model_validate(team)
