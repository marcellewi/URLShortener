"""create urls table

Revision ID: 001
Revises:
Create Date: 2023-07-14 15:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "urls",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("original_url", sa.String(), nullable=False),
        sa.Column("short_code", sa.String(), nullable=False),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_urls_id"), "urls", ["id"], unique=False)
    op.create_index(
        op.f("ix_urls_original_url"), "urls", ["original_url"], unique=False
    )
    op.create_index(op.f("ix_urls_short_code"), "urls", ["short_code"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_urls_short_code"), table_name="urls")
    op.drop_index(op.f("ix_urls_original_url"), table_name="urls")
    op.drop_index(op.f("ix_urls_id"), table_name="urls")
    op.drop_table("urls")
