from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Borrower:
    id: UUID
    name: str
    email: str
    phone: str
    created_at: datetime
    updated_at: datetime
