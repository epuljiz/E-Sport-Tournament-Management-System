from typing import AsyncGenerator
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.errors import AppError
from app.core.jwt import decode_token
from app.models.user import User
from app.repositories import user_repo

_bearer_scheme = HTTPBearer(auto_error=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency koja daje DB sesiju za svaki request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Dependency koja izvlači i validira korisnika iz JWT tokena."""
    if credentials is None:
        raise AppError("invalid_credentials", "Token nije poslan", 401)

    try:
        payload = decode_token(credentials.credentials)
    except JWTError:
        raise AppError("token_expired", "Token je istekao ili nije valjan", 401)

    if payload.get("type") != "access":
        raise AppError("invalid_credentials", "Token nije access tipa", 401)

    user = await user_repo.get_by_id(db, int(payload["sub"]))
    if not user or not user.is_active:
        raise AppError("invalid_credentials", "Korisnik ne postoji ili je deaktiviran", 401)

    return user
