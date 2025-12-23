from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import List
from APP.domain.entities.author import Author
from APP.repositories.Interfaces.author_repositories import AuthorRepository
from APP.models.author_model import AuthorModel
from APP.models.book_model import BookModel
from APP.models.loans_model import LoanModel


class AuthorSQLRepository(AuthorRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_authors(self) -> List[Author]:
        result = await self.session.execute(select(AuthorModel))
        authors = result.scalars().all()
        return [
            Author(
                id=a.id,
                name=a.name,
                bio=a.bio,
                created_at=a.created_at,
                updated_at=a.updated_at,
            )
            for a in authors
        ]

    async def get_author_details(self, author_id: UUID) -> Author:
        a = await self.session.get(AuthorModel, author_id)
        if a is None:
            return None
        return Author(
            id=a.id,
            name=a.name,
            bio=a.bio,
            created_at=a.created_at,
            updated_at=a.updated_at,
        )

    async def create_author(self, author: Author) -> Author:
        db_author = AuthorModel(
            id=author.id,
            name=author.name,
            bio=author.bio,
            created_at=author.created_at,
            updated_at=author.updated_at,
        )
        self.session.add(db_author)
        await self.session.commit()
        await self.session.refresh(db_author)
        return Author(
            id=db_author.id,
            name=db_author.name,
            bio=db_author.bio,
            created_at=db_author.created_at,
            updated_at=db_author.updated_at,
        )

    async def update_author(self, author_id: UUID, author: Author) -> Author:
        db_author = await self.session.get(AuthorModel, author_id)
        db_author.name = author.name
        db_author.bio = author.bio
        db_author.updated_at = author.updated_at
        self.session.add(db_author)
        await self.session.commit()
        await self.session.refresh(db_author)
        return Author(
            id=db_author.id,
            name=db_author.name,
            bio=db_author.bio,
            created_at=db_author.created_at,
            updated_at=db_author.updated_at,
        )

    async def delete_author(self, author_id: UUID) -> None:
        db_author = await self.session.get(AuthorModel, author_id)
        if db_author:
            await self.session.delete(db_author)
            await self.session.commit()

    async def has_loans(self, author_id: UUID) -> bool:
        stmt = (
            select(LoanModel)
            .join(BookModel, LoanModel.book_id == BookModel.id)
            .where(BookModel.author_id == author_id)
        )
        result = await self.session.execute(stmt)
        return result.first() is not None

    async def has_books(self, author_id: UUID) -> bool:
        stmt = select(BookModel).where(BookModel.author_id == author_id)
        result = await self.session.execute(stmt)
        return result.first() is not None
