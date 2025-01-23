from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Table

association_table = Table(
    'association_table',
    Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)