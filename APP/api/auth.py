from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from APP.core.database import get_db
from APP.core.security.passwords import hash_password
from APP.models.user_model import UserModel
from APP.repositories.sqlalchemy.users_sqlRepository import UserSQLRepository
from APP.schemas.auth_schema import LoginRequest, LoginResponse
from APP.services.auth_service import AuthService
from APP.core.events import dispatch_internal_event
from APP.core.internal_events import AuthFailed

router = APIRouter()


async def get_auth_service(session: AsyncSession = Depends(get_db)) -> AuthService:
    user_repo = UserSQLRepository(session)
    service = AuthService(user_repo)
    return service


@router.post("/auth/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.authenticate_user(request.username, request.password)
    if not user:
        await dispatch_internal_event(
            AuthFailed(
                component="Security",
                reason="Missing credentials",
                data={"auth_type": "Authentication"},
            )
        )
        raise HTTPException(status_code=401, detail="Missing credentials")

    token = await service.login_user(user)
    return LoginResponse(access_token=token)


@router.post("/auth/register", response_model=LoginResponse)
async def register(
    request: LoginRequest,
    session: AsyncSession = Depends(get_db),
):
    user_repo = UserSQLRepository(session)
    existing_user = await user_repo.get_user_by_username(request.username)
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    user = UserModel(
        id=uuid4(),
        username=request.username,
        password_hash=hash_password(request.password),
        is_active=True,
    )
    new_user = await user_repo.create_user(user)

    service = AuthService(user_repo)
    token = await service.login_user(new_user)
    return LoginResponse(access_token=token)
