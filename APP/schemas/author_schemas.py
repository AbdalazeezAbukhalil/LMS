from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from APP.schemas.book_schema import BookReadSchema


class AuthorBaseSchema(BaseModel):
    bio: str = Field(..., min_length=10)
    name: str = Field(..., min_length=2)


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorUpdateSchema(AuthorBaseSchema):
    pass


class AuthorReadSchema(AuthorBaseSchema):
    created_at: datetime
    id: UUID
    updated_at: datetime

    class Config:
        orm_mode = True


class AuthorWithBooksSchema(AuthorReadSchema):
    books: List[BookReadSchema] = []
