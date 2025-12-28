from datetime import timedelta

from APP.core.security.jwt import create_access_token
from APP.core.security.passwords import verify_password
from APP.repositories.sqlalchemy.users_sqlRepository import UserSQLRepository


class AuthService:
    def __init__(self, user_repository: UserSQLRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_repository.get_user_by_username(username)
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        if not user.is_active:
            return None

        return user

    async def login_user(self, user):
        token_data = {
            "sub": str(user.id),
            "username": user.username,
        }
        access_token = create_access_token(
            data=token_data, expires_delta=timedelta(hours=1)
        )  # 1hour validity
        return access_token
