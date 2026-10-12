"""added stock price

Revision ID: d3f8a1b2c4e5
Revises: 9a428b0c05f9
Create Date: 2026-09-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3f8a1b2c4e5'
down_revision: Union[str, Sequence[str], None] = '9a428b0c05f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('stockprice',
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('current_price', sa.Numeric(10, 2), nullable=False),
    sa.Column('last_updated', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('symbol')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('stockprice')
