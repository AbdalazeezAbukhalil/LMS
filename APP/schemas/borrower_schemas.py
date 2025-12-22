from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class BorrowerBaseSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    created_at: datetime
    updated_at: datetime  

class BorrowerCreateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str

class BorrowerUpdateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str    

class BorrowerReadSchema(BorrowerBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
