from app.backend.db import Base
from app.models.association import association_table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Column, Integer, String, DateTime, func
import datetime
from .tag import Tag


class Post(Base):
    __tablename__= 'posts'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now())

    tags: Mapped[list['Tag']] = relationship(
        secondary=association_table,
        back_populates="posts",
        lazy="select"
    )