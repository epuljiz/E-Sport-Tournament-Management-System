"""add players table

Revision ID: 002
Revises: 001
Create Date: 2026-04-12

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(length=80), nullable=False),
        sa.Column("last_name", sa.String(length=80), nullable=False),
        sa.Column("nickname", sa.String(length=50), nullable=False),
        sa.Column("position", sa.String(length=50), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=False),
        sa.Column("nationality", sa.String(length=50), nullable=True),
        sa.Column("team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=False),
        sa.UniqueConstraint("nickname"),
    )

def downgrade() -> None:
    op.drop_table("players")
