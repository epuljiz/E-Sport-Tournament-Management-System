import re
import unicodedata
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import AppError
from app.core.security import hash_password
from app.models.team import Team
from app.models.user import User
from app.repositories import team_repo, user_repo

def _slugify(text: str) -> str:
    """Pretvori naziv tima u početni username: 'G2 Esports' → 'g2-esports'."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")

async def create_team(db: AsyncSession, name: str, password: str, organization_name: str | None = None) -> tuple[Team, User]:
    """Kreira tim i automatski generira admin korisnika za taj tim."""
    existing = await team_repo.get_by_name(db, name)
    if existing:
        raise AppError("duplicate", f"Tim '{name}' već postoji", 409)

    username = _slugify(name)
    existing_user = await user_repo.get_by_username(db, username)
    if existing_user:
        username = f"{username}-1" # Jednostavan fallback ako username postoji

    team = Team(name=name, organization_name=organization_name)
    await team_repo.create(db, team)

    user = User(
        username=username,
        email=f"admin@{username}.gg",
        password_hash=hash_password(password),
        role="team_admin",
        team_id=team.id,
    )
    db.add(user)
    await db.flush()

    return team, user

async def list_teams(db: AsyncSession, current_user: User) -> list[Team]:
    """Admin vidi sve, a team_admin vidi samo svoj tim."""
    if current_user.role == "admin":
        return await team_repo.get_all(db)
    team = await team_repo.get_by_id(db, current_user.team_id)
    return [team] if team else []

async def get_team(db: AsyncSession, team_id: int, current_user: User) -> Team:
    """Dohvaća tim po ID-u uz provjeru prava pristupa."""
    team = await team_repo.get_by_id(db, team_id)
    if not team:
        raise AppError("not_found", "Tim nije pronađen", 404)
    
    if current_user.role == "team_admin" and current_user.team_id != team_id:
        raise AppError("forbidden", "Nemate pristup drugom timu", 403)
    
    return team
