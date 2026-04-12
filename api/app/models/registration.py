from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.tournament import Tournament
    from app.models.team import Team

class TournamentRegistration(Base):
    __tablename__ = "tournament_registrations"
    __table_args__ = (UniqueConstraint("team_id", "tournament_id", name="uq_team_tournament"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"), nullable=False)
    
    status: Mapped[str] = mapped_column(String(20), default="active")
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    team: Mapped[Team] = relationship()
    tournament: Mapped[Tournament] = relationship(back_populates="registrations")
