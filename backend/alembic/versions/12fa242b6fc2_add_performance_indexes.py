"""add_performance_indexes

Revision ID: 12fa242b6fc2
Revises: ab9e3cd2cf19
Create Date: 2025-12-05 13:46:16.736056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12fa242b6fc2'
down_revision: Union[str, Sequence[str], None] = 'ab9e3cd2cf19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Indexes on media_relations
    op.create_index('idx_media_relations_source', 'media_relations', ['source_media_id'])
    op.create_index('idx_media_relations_related', 'media_relations', ['related_media_id'])
    op.create_index('idx_media_relations_type', 'media_relations', ['relation_type'])
    op.create_index('idx_media_relations_composite', 'media_relations', ['source_media_id', 'relation_type'])
    
    # Indexes on anime table
    op.create_index('idx_anime_type', 'anime', ['type'])
    op.create_index('idx_anime_status', 'anime', ['status'])
    op.create_index('idx_anime_rating', 'anime', ['rating'])
    op.create_index('idx_anime_popularity', 'anime', ['popularity'])
    op.create_index('idx_anime_original_format', 'anime', ['original_format'])

def downgrade() -> None:
    op.drop_index('idx_anime_original_format', 'anime')
    op.drop_index('idx_anime_popularity', 'anime')
    op.drop_index('idx_anime_rating', 'anime')
    op.drop_index('idx_anime_status', 'anime')
    op.drop_index('idx_anime_type', 'anime')
    op.drop_index('idx_media_relations_composite', 'media_relations')
    op.drop_index('idx_media_relations_type', 'media_relations')
    op.drop_index('idx_media_relations_related', 'media_relations')
    op.drop_index('idx_media_relations_source', 'media_relations')