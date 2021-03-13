from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from base import Base

class Test(Base):

    __tablename__ = 'test'
    test_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # TODO: create a __repr__ function
