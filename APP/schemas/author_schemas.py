# APP/schemas/author_schemas.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AuthorBaseSchema(BaseModel):
    name: str
    bio: str

class AuthorCreateSchema(AuthorBaseSchema):
    pass

class AuthorUpdateSchema(AuthorBaseSchema):
    pass

class AuthorReadSchema(AuthorBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
