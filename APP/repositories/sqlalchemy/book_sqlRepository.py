from typing import List
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload

from APP.domain.entities.books import Book
from APP.domain.exceptions import ISBNAlreadyExistsError
from APP.models.book_model import BookModel
from APP.repositories.Interfaces.book_repositories import BookRepository


class BookSQLRepository(BookRepository):
    def __init__(self, session: Session):
        self.session = session

    async def create_book(self, book: Book) -> Book:
        db_book = BookModel(
            id=book.id,
            title=book.title,
            ISBN=book.ISBN,
            published_date=book.published_date,
            author_id=book.author_id,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )
        self.session.add(db_book)
        try:
            await self.session.commit()
            await self.session.refresh(db_book)
        except IntegrityError:  # Handle unique constraint violation
            await self.session.rollback()
            raise ISBNAlreadyExistsError(book.ISBN)

        return await self.get_book_details(db_book.id)

    async def get_books(self) -> List[Book]:
        stmt = select(BookModel).options(joinedload(BookModel.author))
        result = await self.session.execute(stmt)
        books = result.scalars().all()
        return [
            Book(
                id=b.id,
                title=b.title,
                ISBN=b.ISBN,
                published_date=b.published_date,
                author_id=b.author_id,
                created_at=b.created_at,
                updated_at=b.updated_at,
                author_name=b.author.name if b.author else "Unknown",
            )
            for b in books
        ]

    async def get_book_details(self, book_id: UUID) -> Book:
        stmt = (
            select(BookModel)
            .options(joinedload(BookModel.author))
            .where(BookModel.id == book_id)
        )
        result = await self.session.execute(stmt)
        b = result.scalar_one_or_none()
        if b is None:
            return None
        return Book(
            id=b.id,
            title=b.title,
            ISBN=b.ISBN,
            published_date=b.published_date,
            author_id=b.author_id,
            created_at=b.created_at,
            updated_at=b.updated_at,
            author_name=b.author.name if b.author else "Unknown",
        )

    async def update_book(self, book_id: UUID, book: Book) -> Book:
        db_book = await self.session.get(BookModel, book_id)
        db_book.title = book.title
        db_book.ISBN = book.ISBN
        db_book.published_date = book.published_date
        db_book.author_id = book.author_id
        db_book.updated_at = book.updated_at
        self.session.add(db_book)
        try:
            await self.session.commit()
            await self.session.refresh(db_book)
        except IntegrityError:  # Handle unique constraint violation
            await self.session.rollback()
            raise ISBNAlreadyExistsError(book.ISBN)

        return await self.get_book_details(db_book.id)

    async def delete_book(self, book_id: UUID) -> None:
        db_book = await self.session.get(BookModel, book_id)
        if db_book:
            await self.session.delete(db_book)
            await self.session.commit()
