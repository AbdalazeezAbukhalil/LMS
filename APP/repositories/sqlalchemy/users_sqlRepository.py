from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from APP.models.user_model import UserModel
from fastapi import HTTPException


class UserSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_username(self, username: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user: UserModel) -> UserModel | None:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_id(self, user_id: UUID) -> UserModel | None:
        return await self.session.get(UserModel, user_id)
