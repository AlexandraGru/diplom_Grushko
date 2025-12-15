"""Change customer_type to Enum

Revision ID: 8444fc2489fa
Revises: a1b2c3d4e5f6
Create Date: 2025-12-15 19:07:41.878169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8444fc2489fa'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Так как используется native_enum=False, в PostgreSQL это будет VARCHAR
    # Но нужно добавить CHECK constraint для валидации значений
    # Сначала добавляем CHECK constraint для ограничения допустимых значений
    op.execute("""
        ALTER TABLE customers 
        ADD CONSTRAINT check_customer_type 
        CHECK (customer_type IN ('legal_entity', 'individual'))
    """)
    
    # Если есть старые данные с другими значениями, их нужно обновить
    # (опционально, если есть данные)
    # op.execute("UPDATE customers SET customer_type = 'individual' WHERE customer_type NOT IN ('legal_entity', 'individual')")


def downgrade() -> None:
    # Удаляем CHECK constraint
    op.execute("ALTER TABLE customers DROP CONSTRAINT IF EXISTS check_customer_type")

