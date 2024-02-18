"""01_initial-db

Revision ID: e8d0c656a04e
Revises: 23987db4a1c2
Create Date: 2024-02-18 21:46:44.761745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8d0c656a04e'
down_revision: Union[str, None] = '23987db4a1c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('id_user', sa.UUID(), nullable=False))
    op.drop_constraint('file_owner_fkey', 'file', type_='foreignkey')
    op.create_foreign_key(None, 'file', 'user', ['id_user'], ['id'], ondelete='CASCADE')
    op.drop_column('file', 'owner')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('owner', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'file', type_='foreignkey')
    op.create_foreign_key('file_owner_fkey', 'file', 'user', ['owner'], ['id'], ondelete='CASCADE')
    op.drop_column('file', 'id_user')
    # ### end Alembic commands ###