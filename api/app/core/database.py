from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# 1. Engine — asinkrona veza s PostgreSQL-om
engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

# 2. Session factory — generira nove sesije
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 3. Base — bazna klasa za sve modele
class Base(DeclarativeBase):
    pass
