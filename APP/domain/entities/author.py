# APP/Domain/entities/author.py
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Author:
    id: UUID
    name: str
    bio: str
    created_at: datetime
    updated_at: datetime
