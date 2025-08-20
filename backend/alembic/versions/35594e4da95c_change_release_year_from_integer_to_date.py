"""change release_year from integer to date

Revision ID: 35594e4da95c
Revises: f68e91da1586
Create Date: 2025-08-19 15:23:58.956039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = '35594e4da95c'
down_revision: Union[str, Sequence[str], None] = 'f68e91da1586'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add a temporary column with Date type
    op.add_column('anime', sa.Column('release_year_temp', sa.Date(), nullable=True))
    
    # Convert existing data (assuming January 1st for each year)
    connection = op.get_bind()
    connection.execute(
        text("UPDATE anime SET release_year_temp = CAST(release_year || '-01-01' AS DATE) WHERE release_year IS NOT NULL")
    )
    
    # Drop the old integer column
    op.drop_column('anime', 'release_year')
    
    # Rename the temp column to the original name
    op.alter_column('anime', 'release_year_temp', new_column_name='release_year')


def downgrade() -> None:
    """Downgrade schema."""
    # Add a temporary column with Integer type
    op.add_column('anime', sa.Column('release_year_temp', sa.Integer(), nullable=True))
    
    # Convert data back (extract year from date)
    connection = op.get_bind()
    connection.execute(
        text("UPDATE anime SET release_year_temp = EXTRACT(YEAR FROM release_year) WHERE release_year IS NOT NULL")
    )
    
    # Drop the date column
    op.drop_column('anime', 'release_year')
    
    # Rename temp column back to original name
    op.alter_column('anime', 'release_year_temp', new_column_name='release_year')