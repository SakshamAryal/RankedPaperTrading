"""added net_deposited to portfolio

Revision ID: e7b2c9d4a1f3
Revises: d3f8a1b2c4e5
Create Date: 2026-10-26 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7b2c9d4a1f3'
down_revision: Union[str, Sequence[str], None] = 'd3f8a1b2c4e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('portfolio', sa.Column('net_deposited', sa.Numeric(10, 2), server_default='0', nullable=False))
    # total_balance has only changed on create/deposit/withdraw so far, so it equals net deposited
    op.execute("UPDATE portfolio SET net_deposited = total_balance")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('portfolio', 'net_deposited')
