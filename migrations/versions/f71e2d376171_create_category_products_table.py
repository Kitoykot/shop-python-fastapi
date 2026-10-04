"""create category products table

Revision ID: f71e2d376171
Revises: 13b238a2cd62
Create Date: 2026-09-16 16:16:25.323234

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f71e2d376171'
down_revision: Union[str, Sequence[str], None] = '13b238a2cd62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'category_products',
        sa.Column(
            'category_id',
            sa.Integer(),
            sa.ForeignKey('categories.id', ondelete='CASCADE'),
            primary_key=True,
        ),
        sa.Column(
            'product_id',
            sa.Integer(),
            sa.ForeignKey('products.id', ondelete='CASCADE'),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table('category_products', if_exists=True)
