"""Add is_countable field and remove quantity from products

Revision ID: d9cb79a966df
Revises: 8444fc2489fa
Create Date: 2025-12-15 19:13:32.909548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9cb79a966df'
down_revision: Union[str, None] = '8444fc2489fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем поле is_countable
    op.add_column('products', sa.Column('is_countable', sa.Boolean(), nullable=False, server_default='true'))
    
    # Удаляем поле quantity
    op.drop_column('products', 'quantity')


def downgrade() -> None:
    # Возвращаем поле quantity
    op.add_column('products', sa.Column('quantity', sa.Integer(), nullable=False, server_default='0'))
    
    # Удаляем поле is_countable
    op.drop_column('products', 'is_countable')

