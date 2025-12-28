from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Loan:
    book_id: UUID
    borrower_id: UUID
    created_at: datetime
    id: UUID
    loan_date: datetime
    return_date: datetime
    updated_at: datetime
