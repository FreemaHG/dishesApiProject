"""Add Dish model

Revision ID: e0bb34ba6667
Revises: 885354e1d999
Create Date: 2024-01-19 23:49:43.889253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0bb34ba6667'
down_revision: Union[str, None] = '885354e1d999'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dish',
    sa.Column('price', sa.Float(precision=2), nullable=False),
    sa.Column('submenu_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=280), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['submenu_id'], ['submenu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dish_id'), 'dish', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dish_id'), table_name='dish')
    op.drop_table('dish')
    # ### end Alembic commands ###
