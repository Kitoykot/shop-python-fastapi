"""create order_items table

Revision ID: 9b624e0f13ad
Revises: 15280868bca9
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '9b624e0f13ad'
down_revision: Union[str, Sequence[str], None] = '15280868bca9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('product_name', sa.String(length=256), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('count', sa.SmallInteger(), nullable=False),
        sa.CheckConstraint('count > 0', name='check_order_items_count_positive'),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(
            ['product_id'],
            ['products.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('order_items', if_exists=True)
