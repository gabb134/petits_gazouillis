"""table utilisateurs ajouter avatar

Revision ID: bfae7a4f15cf
Revises: 3de09badd5ec
Create Date: 2020-09-14 00:43:33.376684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfae7a4f15cf'
down_revision = '3de09badd5ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('utilisateur', sa.Column('a_propos_de_moi', sa.String(length=140), nullable=True))
    op.add_column('utilisateur', sa.Column('avatar', sa.Text(length=131072), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('utilisateur', 'avatar')
    op.drop_column('utilisateur', 'a_propos_de_moi')
    # ### end Alembic commands ###
