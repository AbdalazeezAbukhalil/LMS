from typing import List
from uuid import UUID
from fastapi import HTTPException
from APP.domain.entities.books import Book
from APP.repositories.Interfaces.book_repositories import BookRepository
from APP.services.author_service import AuthorService

class BookService:
    def __init__(self, book_repository: BookRepository, author_service: AuthorService):
        self.book_repository = book_repository
        self.author_service = author_service

    async def get_books(self) -> List[Book]:
        return await self.book_repository.get_books()

    async def get_book_details(self, book_id: UUID) -> Book:
        return await self.book_repository.get_book_details(book_id)

    async def create_book(self, book: Book) -> Book:
        author = await self.author_service.get_author_details(book.author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return await self.book_repository.create_book(book)

    async def update_book(self, book_id: UUID, book: Book) -> Book:
        author = await self.author_service.get_author_details(book.author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return await self.book_repository.update_book(book_id, book)

    async def delete_book(self, book_id: UUID) -> None:
        return await self.book_repository.delete_book(book_id)