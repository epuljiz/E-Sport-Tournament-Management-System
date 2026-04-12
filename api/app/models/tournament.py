from __future__ import annotations
from datetime import date, datetime
from typing import TYPE_CHECKING
from sqlalchemy import Date, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.registration import TournamentRegistration

class Tournament(Base):
    __tablename__ = "tournaments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    game: Mapped[str] = mapped_column(String(100), nullable=False) # npr. Counter-Strike 2
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=False)

    prelim_deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    final_deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    registrations: Mapped[list[TournamentRegistration]] = relationship(
        back_populates="tournament"
    )
