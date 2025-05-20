"""add_is_custom_column

Revision ID: 98f76ab254e2
Revises: fca45759e76d
Create Date: 2023-06-15 10:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "98f76ab254e2"
down_revision: Union[str, None] = "fca45759e76d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add is_custom column with default value of False
    op.add_column(
        "urls",
        sa.Column("is_custom", sa.Boolean(), nullable=False, server_default="false"),
    )

    # Create index on is_custom
    op.create_index(op.f("ix_urls_is_custom"), "urls", ["is_custom"], unique=False)


def downgrade() -> None:
    # Drop index first
    op.drop_index(op.f("ix_urls_is_custom"), table_name="urls")

    # Drop column
    op.drop_column("urls", "is_custom")
