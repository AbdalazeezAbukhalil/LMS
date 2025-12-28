import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from APP.core.database import Base


class LoanModel(Base):
    __tablename__ = "loans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    borrower_id = Column(UUID(as_uuid=True), ForeignKey("borrowers.id"), nullable=False)
    loan_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    book = relationship("BookModel", back_populates="loans")
    borrower = relationship("BorrowerModel", back_populates="loans")
