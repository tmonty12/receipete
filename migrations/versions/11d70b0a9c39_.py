"""empty message

Revision ID: 11d70b0a9c39
Revises: 29ce3cb2764d
Create Date: 2023-03-12 17:08:40.791023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11d70b0a9c39'
down_revision = '29ce3cb2764d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('allergy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('allergy', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_allergy_type'), ['type'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('allergy', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_allergy_type'))

    op.drop_table('allergy')
    # ### end Alembic commands ###