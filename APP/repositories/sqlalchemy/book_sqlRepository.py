from sqlalchemy.orm import Session
from sqlalchemy.future import select
from APP.domain.entities.books import Book
from APP.repositories.Interfaces.book_repositories import BookRepository
from uuid import UUID
from typing import List
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from APP.models.book_model import BookModel
class BookSQLRepository(BookRepository):
    def __init__(self, session: Session):
        self.session=session
    
    async def create_book(self, book: Book) -> Book:
        db_book = BookModel(
            id=book.id,
            title=book.title,
            ISBN=book.ISBN,
            published_date=book.published_date,
            author_id=book.author_id,
            created_at=book.created_at,
            updated_at=book.updated_at
        )
        self.session.add(db_book)
        try:
            await self.session.commit()
            await self.session.refresh(db_book)
        except IntegrityError:                         ## Handle unique constraint violation
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="ISBN already exists")
        return Book(
            id=db_book.id,
            title=db_book.title,
            ISBN=db_book.ISBN,
            published_date=db_book.published_date,
            author_id=db_book.author_id,
            created_at=db_book.created_at,
            updated_at=db_book.updated_at
        )
    
    async def get_books(self) -> List[Book]:
        result = await self.session.execute(select(BookModel))
        books = result.scalars().all()
        return [Book(
            id=b.id,
            title=b.title,
            ISBN=b.ISBN,
            published_date=b.published_date,
            author_id=b.author_id,
            created_at=b.created_at,
            updated_at=b.updated_at
        ) for b in books]

    async def get_book_details(self, book_id: UUID) -> Book:
        b = await self.session.get(BookModel, book_id)
        if b is None:
            return None
        return Book(
            id=b.id,
            title=b.title,
            ISBN=b.ISBN,
            published_date=b.published_date,
            author_id=b.author_id,
            created_at=b.created_at,
            updated_at=b.updated_at
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
        except IntegrityError:                         ## Handle unique constraint violation
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="ISBN already exists")

        return Book(
            id=db_book.id,
            title=db_book.title,
            ISBN=db_book.ISBN,
            published_date=db_book.published_date,
            author_id=db_book.author_id,
            created_at=db_book.created_at,
            updated_at=db_book.updated_at
        )

    async def delete_book(self, book_id: UUID) -> None:
        db_book = await self.session.get(BookModel, book_id)
        if db_book:
            await self.session.delete(db_book)
            await self.session.commit()
