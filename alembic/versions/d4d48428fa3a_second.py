"""second

Revision ID: d4d48428fa3a
Revises: f4f3d56df648
Create Date: 2025-04-06 21:03:22.566437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4d48428fa3a'
down_revision: Union[str, None] = 'f4f3d56df648'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
