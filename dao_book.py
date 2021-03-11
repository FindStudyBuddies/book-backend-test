from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from base import Base

class Book(Base):  
    __tablename__ = 'books'

    book_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey('authors.author_id'), nullable=False)
    first_sentence = Column(String)
    published = Column(Integer)
    author = relationship("Author", back_populates="books")
    # TODO: create a __repr__ function
