# migrations/versions/f9c217dece91_add_nickname_column.py
from alembic import op  # type: ignore
import sqlalchemy as sa  # type: ignore
from sqlalchemy.sql import table, column  # type: ignore

# revision identifiers, used by Alembic.
revision = 'f9c217dece91'
down_revision = '1c67667f4d44'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. Add the column, temporarily allowing NULL
    op.add_column('students', sa.Column('nickname', sa.String(), nullable=True))

    # Import table/column definitions to execute UPDATE statements
    students_table = table('students', column('nickname', sa.String))

    # 2. Update all existing rows, setting a default value ('No Nickname')
    # This ensures no rows violate the NOT NULL constraint in the next step.
    op.execute(
        students_table.update().where(students_table.c.nickname == sa.null()).values(nickname='No Nickname')
    )

    # 3. Alter the column to enforce the NOT NULL constraint
    op.alter_column('students', 'nickname', existing_type=sa.String(), nullable=False)


def downgrade() -> None:
    # To reverse this, we only need to drop the column.
    op.drop_column('students', 'nickname')