from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from APP.core.config import settings
from APP.core.database import get_db
from APP.core.events import dispatch_internal_event
from APP.core.internal_events import AuthFailed
from APP.core.security.jwt import verify_token
from APP.models.user_model import UserModel
from APP.repositories.sqlalchemy.users_sqlRepository import UserSQLRepository

security = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def verify_jwt(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
):

    try:
        token = credentials.credentials
        payload = verify_token(token)
        return payload
    except ValueError as e:
        await dispatch_internal_event(
            AuthFailed(
                component="Security",
                reason=str(e),
                data={"auth_type": "JWT"},
            )
        )
        raise HTTPException(status_code=401, detail=str(e))
    except Exception:
        await dispatch_internal_event(
            AuthFailed(
                component="Security",
                reason="Invalid token",
                data={"auth_type": "JWT"},
            )
        )
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    payload: dict = Depends(verify_jwt), session: AsyncSession = Depends(get_db)
) -> UserModel:
    user_repo = UserSQLRepository(session)
    user_id = payload.get("sub")
    if not user_id:
        await dispatch_internal_event(
            AuthFailed(
                component="Security",
                reason="Invalid token payload",
                data={"auth_type": "JWT", "payload": payload},
            )
        )
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = await user_repo.get_user_by_id(UUID(user_id))
    if not user:
        await dispatch_internal_event(
            AuthFailed(
                component="Security",
                reason="User not found",
                data={"auth_type": "JWT", "user_id": user_id},
            )
        )
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def verify_api_key(x_api_key: Optional[str] = Security(api_key_header)):
    if not x_api_key:
        await dispatch_internal_event(
            AuthFailed(
                component="Security",
                reason="Missing API key",
                data={"auth_type": "APIKey"},
            )
        )
        raise HTTPException(status_code=401, detail="Missing API key")

    if x_api_key != settings.api_key:
        await dispatch_internal_event(
            AuthFailed(
                component="Security",
                reason="Invalid API key",
                data={"auth_type": "APIKey"},
            )
        )
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
