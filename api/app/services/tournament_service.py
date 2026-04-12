from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import AppError
from app.models.tournament import Tournament
from app.repositories import tournament_repo
from app.schemas.tournament import TournamentCreate

async def list_tournaments(db: AsyncSession) -> list[Tournament]:
    """Lista svih turnira."""
    return await tournament_repo.get_all(db)

async def get_tournament(db: AsyncSession, tournament_id: int) -> Tournament:
    """Dohvaćanje turnira ili 404."""
    tournament = await tournament_repo.get_by_id(db, tournament_id)
    if not tournament:
        raise AppError("not_found", "Turnir nije pronađen", 404)
    return tournament

async def create_tournament(db: AsyncSession, body: TournamentCreate) -> Tournament:
    """Admin kreira turnir."""
    tournament = Tournament(
        name=body.name,
        game=body.game,
        start_date=body.start_date,
        location=body.location,
        prelim_deadline=body.prelim_deadline,
        final_deadline=body.final_deadline
    )
    return await tournament_repo.create(db, tournament)
