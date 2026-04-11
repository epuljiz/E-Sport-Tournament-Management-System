from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.team import Team

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    position: Mapped[str] = mapped_column(String(50), nullable=False) # npr. IGL, AWPer, Entry Fragger
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    nationality: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    team: Mapped[Team] = relationship(back_populates="members")
