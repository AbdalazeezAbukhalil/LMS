from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class LoanBaseSchema(BaseModel):
    book_id: UUID
    borrower_id: UUID
    created_at: datetime
    loan_date: datetime
    return_date: Optional[datetime] = None
    updated_at: datetime


class LoanCreateSchema(BaseModel):
    book_id: UUID
    borrower_id: UUID


class LoanReadSchema(LoanBaseSchema):
    created_at: datetime
    id: UUID
    updated_at: datetime



# update schema isn't needed here since we only update the returned_date
