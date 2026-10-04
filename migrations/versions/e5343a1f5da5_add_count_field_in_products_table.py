"""Add count field in products table

Revision ID: e5343a1f5da5
Revises: 47c3d5a1a668
Create Date: 2026-09-11 19:52:28.578587

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e5343a1f5da5'
down_revision: Union[str, Sequence[str], None] = '47c3d5a1a668'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'products', sa.Column('count', sa.SmallInteger(), server_default='0', default=0)
    )


def downgrade() -> None:
    op.drop_column('products', 'count')
