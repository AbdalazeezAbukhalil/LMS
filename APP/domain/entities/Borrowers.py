from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from APP.domain.entities.Loans import Loan


@dataclass
class Borrower:
    created_at: datetime
    email: str
    id: UUID
    name: str
    phone: str
    updated_at: datetime
    loans: Optional[List[Loan]] = None
