"""add tournaments and registrations

Revision ID: 003
Revises: 002
Create Date: 2026-04-12

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Tournaments table
    op.create_table(
        "tournaments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("game", sa.String(length=100), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("location", sa.String(length=200), nullable=False),
        sa.Column("prelim_deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("final_deadline", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. Tournament Registrations table
    op.create_table(
        "tournament_registrations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("tournament_id", sa.Integer(), sa.ForeignKey("tournaments.id"), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="active", nullable=False),
        sa.Column("registered_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("team_id", "tournament_id", name="uq_team_tournament"),
    )

def downgrade() -> None:
    op.drop_table("tournament_registrations")
    op.drop_table("tournaments")
