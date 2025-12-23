from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from APP.core.database import Base
from APP.models.author_model import AuthorModel
from sqlalchemy.orm import relationship

class BookModel(Base):
    __tablename__="books"
    id = Column (UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    title = Column(String, nullable=False)
    ISBN = Column(String, nullable=False, unique=True)
    published_date = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    author_id = Column(UUID(as_uuid=True),ForeignKey("authors.id")  ,nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    author = relationship("AuthorModel", back_populates="books")
    
    loans = relationship("LoanModel", back_populates="book", cascade="all, delete-orphan")