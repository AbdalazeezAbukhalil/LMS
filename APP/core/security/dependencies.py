from fastapi import HTTPException, Depends, Header, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from APP.core.security.jwt import verify_token
from APP.repositories.sqlalchemy.users_sqlRepository import UserSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession
from APP.core.database import get_db
from APP.models.user_model import UserModel
from APP.core.config import settings
from uuid import UUID

security = HTTPBearer()
api_key_header = APIKeyHeader(name="x-api-key")


async def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        payload = verify_token(token)
        return payload
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    payload: dict = Depends(verify_jwt), session: AsyncSession = Depends(get_db)
) -> UserModel:
    user_repo = UserSQLRepository(session)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = await user_repo.get_user_by_id(UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def verify_api_key(x_api_key: str = Security(api_key_header)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
