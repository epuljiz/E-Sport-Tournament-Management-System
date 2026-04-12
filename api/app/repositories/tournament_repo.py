from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tournament import Tournament

async def get_all(db: AsyncSession) -> list[Tournament]:
    """Dohvati sve turnire poređane po datumu."""
    result = await db.execute(select(Tournament).order_by(Tournament.start_date))
    return list(result.scalars().all())

async def get_by_id(db: AsyncSession, tournament_id: int) -> Tournament | None:
    """Dohvati turnir po ID-u."""
    result = await db.execute(select(Tournament).where(Tournament.id == tournament_id))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, tournament: Tournament) -> Tournament:
    """Spremi novi turnir."""
    db.add(tournament)
    await db.flush()
    return tournament
