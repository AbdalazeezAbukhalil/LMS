import re
from datetime import datetime
from typing import Annotated, List
from uuid import UUID

from pydantic import AfterValidator, BaseModel, BeforeValidator, EmailStr, Field

from APP.schemas.loans_schemas import LoanReadSchema


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
    created_at: datetime
    email: EmailStr
    name: str
    phone: PhoneStr
    updated_at: datetime


class BorrowerCreateSchema(BaseModel):
    email: EmailStr
    name: str
    phone: PhoneStr


class BorrowerUpdateSchema(BaseModel):
    email: EmailStr
    name: str
    phone: PhoneStr


class BorrowerReadSchema(BorrowerBaseSchema):
    created_at: datetime
    id: UUID
    updated_at: datetime


class BorrowerWithLoansSchema(BorrowerReadSchema):
    loans: List[LoanReadSchema] = []
