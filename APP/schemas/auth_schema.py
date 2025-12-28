from pydantic import BaseModel


class LoginRequest(BaseModel):
    password: str
    username: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
