from pydantic import BaseModel, EmailStr, Field, BeforeValidator, AfterValidator
from uuid import UUID
from datetime import datetime
from typing import Annotated
import re


def clean_phone_number(v: str) -> str:
    if isinstance(v, str):
        # Remove spaces, dashes, and parentheses
        return re.sub(r"[\s\-\(\)]", "", v)
    return v


def validate_phone_format(v: str) -> str:
    if not re.match(r"^\+?[0-9]+$", v):
        raise ValueError(
            "Phone number must be digits only, optionally starting with '+'. Example: +962798637216"
        )
    return v


PhoneStr = Annotated[
    str,
    BeforeValidator(clean_phone_number),
    AfterValidator(validate_phone_format),
    Field(min_length=10, max_length=13),
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
