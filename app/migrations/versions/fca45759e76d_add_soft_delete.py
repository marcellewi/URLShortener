"""add_soft_delete

Revision ID: fca45759e76d
Revises: 001
Create Date: 2025-05-20 07:50:46.972758

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "fca45759e76d"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_deleted column with default value False
    op.add_column(
        "urls",
        sa.Column(
            "is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
    )
    op.create_index(op.f("ix_urls_is_deleted"), "urls", ["is_deleted"], unique=False)


def downgrade() -> None:
    # Remove the is_deleted column on downgrade
    op.drop_index(op.f("ix_urls_is_deleted"), table_name="urls")
    op.drop_column("urls", "is_deleted")
