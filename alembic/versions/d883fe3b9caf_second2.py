"""second2

Revision ID: d883fe3b9caf
Revises: d4d48428fa3a
Create Date: 2025-04-06 21:06:48.859750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd883fe3b9caf'
down_revision: Union[str, None] = 'd4d48428fa3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
