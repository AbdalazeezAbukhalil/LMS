from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class LoanBaseSchema(BaseModel):
    book_id: UUID
    borrower_id: UUID
    loan_date: datetime
    return_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class LoanCreateSchema(BaseModel):
    book_id: UUID
    borrower_id: UUID
    

class LoanUpdateSchema(BaseModel):
    book_id: UUID
    borrower_id: UUID
    loan_date: datetime
    return_date: datetime

class LoanReadSchema(LoanBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
