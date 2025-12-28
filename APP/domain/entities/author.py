from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from APP.domain.entities.books import Book


@dataclass
class Author:
    bio: str
    created_at: datetime
    id: UUID
    name: str
    updated_at: datetime
    books: Optional[List[Book]] = None
