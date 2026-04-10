import asyncio
import logging
import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine
from app.models.user import User
from app.models.team import Team

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Seed podaci
ADMIN_DATA = {
    "username": "admin",
    "email": "admin@esport.com",
    "password": "admin123",
    "role": "admin"
}

TEAMS = [
    {
        "name": "G2 Esports",
        "organization_name": "G2",
        "admin_username": "g2_admin",
        "admin_email": "contact@g2.gg",
        "admin_password": "team123"
    },
    {
        "name": "Natus Vincere",
        "organization_name": "NaVi",
        "admin_username": "navi_admin",
        "admin_email": "contact@navi.gg",
        "admin_password": "team123"
    }
]

def _hash_pw(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

async def _seed_team(session: AsyncSession, data: dict) -> Team:
    result = await session.execute(select(Team).where(Team.name == data["name"]))
    team = result.scalar_one_or_none()

    if team is None:
        team = Team(
            name=data["name"],
            organization_name=data["organization_name"]
        )
        session.add(team)
        await session.flush()
        logger.info("Kreiran tim: %s", team.name)
    else:
        logger.info("Tim '%s' već postoji.", team.name)

    result = await session.execute(select(User).where(User.username == data["admin_username"]))
    if result.scalar_one_or_none() is None:
        user = User(
            username=data["admin_username"],
            email=data["admin_email"],
            password_hash=_hash_pw(data["admin_password"]),
            role="team_admin",
            team_id=team.id
        )
        session.add(user)
        logger.info("Kreiran team admin: %s", user.username)
    
    return team

async def seed(session: AsyncSession) -> None:
    # 1. Timovi i njihovi admini
    for team_data in TEAMS:
        await _seed_team(session, team_data)

    # 2. Glavni admin
    result = await session.execute(select(User).where(User.username == ADMIN_DATA["username"]))
    if result.scalar_one_or_none() is None:
        admin = User(
            username=ADMIN_DATA["username"],
            email=ADMIN_DATA["email"],
            password_hash=_hash_pw(ADMIN_DATA["password"]),
            role=ADMIN_DATA["role"],
            team_id=None
        )
        session.add(admin)
        logger.info("Kreiran admin: %s", admin.username)

    await session.commit()
    logger.info("Seed završen!")

async def main() -> None:
    async with AsyncSessionLocal() as session:
        await seed(session)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
