from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Book:
    id: UUID
    title: str
    ISBN: str
    published_date: datetime
    author_id: UUID
    created_at: datetime
    updated_at: datetime
