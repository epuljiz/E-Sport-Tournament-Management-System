from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db, require_role
from app.models.user import User
from app.schemas.tournament import TournamentCreate, TournamentResponse
from app.schemas.registration import RegistrationResponse
from app.services import tournament_service, registration_service

router = APIRouter()

# --- Turniri ---

@router.get("/", response_model=list[TournamentResponse])
async def list_tournaments(db: AsyncSession = Depends(get_db)):
    """Lista svih dostupnih turnira."""
    return await tournament_service.list_tournaments(db)

@router.post("/", response_model=TournamentResponse, status_code=201)
async def create_tournament(
    body: TournamentCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    """Admin kreira novi turnir."""
    return await tournament_service.create_tournament(db, body)

@router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(tournament_id: int, db: AsyncSession = Depends(get_db)):
    """Detalji pojedinog turnira."""
    return await tournament_service.get_tournament(db, tournament_id)

# --- Prijave (Registrations) ---

@router.post("/{tournament_id}/registrations", response_model=RegistrationResponse, status_code=201)
async def register_team(
    tournament_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "team_admin")),
):
    """Prijava tima na turnir. Provjeravaju se rokovi i broj igrača."""
    reg = await registration_service.register_team(db, tournament_id, user)
    return RegistrationResponse.from_orm_extra(reg)

@router.get("/{tournament_id}/registrations", response_model=list[RegistrationResponse])
async def list_registrations(
    tournament_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Lista svih prijavljenih timova za turnir."""
    regs = await registration_service.list_registrations(db, tournament_id)
    return [RegistrationResponse.from_orm_extra(r) for r in regs]

@router.post("/{tournament_id}/registrations/{reg_id}/withdraw", status_code=204)
async def withdraw_registration(
    tournament_id: int,
    reg_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "team_admin")),
):
    """Odjava tima s turnira (prije isteka roka)."""
    await registration_service.withdraw_registration(db, tournament_id, reg_id, user)
