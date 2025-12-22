from uuid import UUID
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Loan:
    id: UUID
    book_id: UUID
    borrower_id: UUID
    loan_date: datetime
    return_date: datetime
    created_at: datetime
    updated_at: datetime