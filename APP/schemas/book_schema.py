from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BookBaseSchema(BaseModel):
    title: str
    ISBN: str
    author_id: UUID


class BookCreateSchema(BookBaseSchema):
    pass

class BookUpdateSchema(BookBaseSchema):
    pass

class BookReadSchema(BookBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
