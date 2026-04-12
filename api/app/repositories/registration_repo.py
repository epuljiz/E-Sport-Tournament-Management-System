from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.registration import TournamentRegistration

async def get_by_tournament(
    db: AsyncSession, 
    tournament_id: int, 
    team_id: int | None = None
) -> list[TournamentRegistration]:
    """Dohvati prijave za turnir, opcionalno filtrirano po timu."""
    stmt = select(TournamentRegistration).options(selectinload(TournamentRegistration.team)).where(TournamentRegistration.tournament_id == tournament_id)
    if team_id is not None:
        stmt = stmt.where(TournamentRegistration.team_id == team_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_by_id(db: AsyncSession, reg_id: int) -> TournamentRegistration | None:
    """Dohvati prijavu po ID-u."""
    result = await db.execute(select(TournamentRegistration).options(selectinload(TournamentRegistration.tournament), selectinload(TournamentRegistration.team)).where(TournamentRegistration.id == reg_id))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, reg: TournamentRegistration) -> TournamentRegistration:
    """Spremi novu prijavu."""
    db.add(reg)
    await db.flush()
    return reg
