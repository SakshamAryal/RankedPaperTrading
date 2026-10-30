"""portfolio name unique per user among active portfolios

Revision ID: a4c8e1f6b2d9
Revises: e7b2c9d4a1f3
Create Date: 2026-10-26 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4c8e1f6b2d9'
down_revision: Union[str, Sequence[str], None] = 'e7b2c9d4a1f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('portfolio_name_key', 'portfolio', type_='unique')
    op.drop_constraint('unique_portfolio_name', 'portfolio', type_='unique')
    op.create_index('unique_active_portfolio_name', 'portfolio', ['user_id', 'name'], unique=True,
                    postgresql_where=sa.text('is_active'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('unique_active_portfolio_name', table_name='portfolio')
    op.create_unique_constraint('unique_portfolio_name', 'portfolio', ['user_id', 'name'])
    op.create_unique_constraint('portfolio_name_key', 'portfolio', ['name'])
