from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.team import Team

async def get_all(db: AsyncSession) -> list[Team]:
    """Dohvati sve timove s učitavanjem članova."""
    result = await db.execute(
        select(Team).options(selectinload(Team.members)).order_by(Team.id)
    )
    return list(result.scalars().all())

async def get_by_id(db: AsyncSession, team_id: int) -> Team | None:
    """Dohvati tim po ID-u."""
    result = await db.execute(
        select(Team).options(selectinload(Team.members)).where(Team.id == team_id)
    )
    return result.scalar_one_or_none()

async def get_by_name(db: AsyncSession, name: str) -> Team | None:
    """Dohvati tim po nazivu (za provjeru duplikata)."""
    result = await db.execute(select(Team).where(Team.name == name))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, team: Team) -> Team:
    """Spremi novi tim u bazu."""
    db.add(team)
    await db.flush()
    return team
