"""add content column to post table

Revision ID: 1db8457ade2f
Revises: ae91559c440f
Create Date: 2023-09-04 14:03:02.400635

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1db8457ade2f'
down_revision: Union[str, None] = 'ae91559c440f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
