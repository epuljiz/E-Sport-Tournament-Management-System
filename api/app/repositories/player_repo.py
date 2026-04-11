from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.player import Player

async def get_by_team(
    db: AsyncSession,
    team_id: int,
    limit: int = 20,
    offset: int = 0,
) -> list[Player]:
    """Lista igrača tima s paginacijom."""
    stmt = select(Player).where(Player.team_id == team_id)
    stmt = stmt.order_by(Player.id).limit(limit).offset(offset)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_by_id(db: AsyncSession, player_id: int) -> Player | None:
    """Dohvati igrača po ID-u."""
    result = await db.execute(select(Player).where(Player.id == player_id))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, player: Player) -> Player:
    """Spremi novog igrača."""
    db.add(player)
    await db.flush()
    return player

async def delete(db: AsyncSession, player: Player) -> None:
    """Obriši igrača."""
    await db.delete(player)
