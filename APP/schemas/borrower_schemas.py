from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Annotated
from pydantic import Field

PhoneStr = Annotated[
    str,
    Field(
        min_length=10,
        max_length=15,
        pattern=r"^\+?[0-9]+$"
    )
]
class BorrowerBaseSchema(BaseModel):
    name: str
    email: EmailStr
    phone: PhoneStr
    created_at: datetime
    updated_at: datetime  

class BorrowerCreateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: PhoneStr

class BorrowerUpdateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: PhoneStr    

class BorrowerReadSchema(BorrowerBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
