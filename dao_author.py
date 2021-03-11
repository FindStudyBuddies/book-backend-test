from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from base import Base

class Author(Base):

    __tablename__ = 'authors'

    author_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_first_name = Column(String, nullable=False)
    author_last_name = Column(String)
    books = relationship("Book", back_populates="author")
    # TODO: create a __repr__ function
