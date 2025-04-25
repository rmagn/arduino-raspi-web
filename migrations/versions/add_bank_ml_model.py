"""add bank ml model

Revision ID: add_bank_ml_model
Revises: 
Create Date: 2024-04-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_bank_ml_model'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('bank_ml_models',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vectorizer', sa.LargeBinary(), nullable=False),
        sa.Column('train_data', sa.LargeBinary(), nullable=False),
        sa.Column('train_labels', sa.LargeBinary(), nullable=False),
        sa.Column('train_sub_labels', sa.LargeBinary(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.now),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('bank_ml_models') 