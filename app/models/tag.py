from app.backend.db import Base
from app.models.association import association_table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String


class Tag(Base):
    __tablename__= 'tags'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50))

    post: Mapped[list['Post']] = relationship(
        secondary=association_table,
        back_populates="tags",
        lazy="selectin"
    )