import re
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel


def validate_isbn(v: str) -> str:
    # Remove dashes and spaces
    v = re.sub(r"[\s\-]", "", v)
    if not re.match(r"^(?:\d{10}|\d{13})$", v):
        raise ValueError("ISBN must be 10 or 13 digits")
    return v


ISBNStr = Annotated[str, AfterValidator(validate_isbn)]


class BookBaseSchema(BaseModel):
    author_id: UUID
    ISBN: ISBNStr
    title: str


class BookCreateSchema(BookBaseSchema):
    pass


class BookUpdateSchema(BookBaseSchema):
    pass


class BookReadSchema(BookBaseSchema):
    author_name: str
    created_at: datetime
    id: UUID
    updated_at: datetime

    class Config:
        orm_mode = True
