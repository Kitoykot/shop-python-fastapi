"""create products table

Revision ID: 47c3d5a1a668
Revises:
Create Date: 2026-09-07 20:40:07.099287

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "47c3d5a1a668"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(256), primary_key=False, nullable=False),
        sa.Column("description", sa.Text(), primary_key=False, nullable=True),
        sa.Column("price", sa.Numeric(10, 2), primary_key=False, nullable=False),
        sa.Column(
            "show_in_catalog",
            sa.Boolean(),
            primary_key=False,
            nullable=False,
            default=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("products", if_exists=True)
