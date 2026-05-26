"""add refresh token column in user model

Revision ID: 620fd1c397e7
Revises: 894a8dce1a48
Create Date: 2026-05-22 20:50:41.102726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
# revision identifiers, used by Alembic.
revision: str = '620fd1c397e7'
down_revision: Union[str, Sequence[str], None] = '894a8dce1a48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('refresh_token', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'refresh_token')
