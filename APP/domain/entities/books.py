from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Book:
    author_id: UUID
    created_at: datetime
    id: UUID
    ISBN: str
    published_date: datetime
    title: str
    updated_at: datetime
    author_name: str = ""
