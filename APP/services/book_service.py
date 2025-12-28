from typing import List
from uuid import UUID

from fastapi import HTTPException

from APP.domain.entities.books import Book
from APP.repositories.Interfaces.book_repositories import BookRepository
from APP.repositories.sqlalchemy.loans_sqlRepository import LoansSQLRepository
from APP.services.author_service import AuthorService


class BookService:
    """
    Service layer for managing book-related business logic.
    """

    def __init__(
        self,
        book_repository: BookRepository,
        author_service: AuthorService,
        loans_sqlRepository: LoansSQLRepository,
    ):
        self.book_repository = book_repository
        self.author_service = author_service
        self.loans_sqlRepository = loans_sqlRepository

    async def get_books(self) -> List[Book]:
        """
        Retrieve all books from the repository.
        """
        return await self.book_repository.get_books()

    async def get_book_details(self, book_id: UUID) -> Book:
        """
        Retrieve details for a specific book by its ID.
        """
        return await self.book_repository.get_book_details(book_id)

    async def create_book(self, book: Book) -> Book:
        """
        Create a new book record, ensuring the author exists.
        """
        author = await self.author_service.get_author_details(book.author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return await self.book_repository.create_book(book)

    async def update_book(self, book_id: UUID, book: Book) -> Book:
        """
        Update an existing book's details, ensuring the author exists.
        """
        author = await self.author_service.get_author_details(book.author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return await self.book_repository.update_book(book_id, book)

    async def delete_book(self, book_id: UUID) -> None:
        """
        Delete a book if it has no active loans.
        """
        active_loans = await self.loans_sqlRepository.has_active_loan_for_book(book_id)
        if active_loans:
            raise HTTPException(
                status_code=400, detail="Cannot delete book with active loans"
            )
        await self.book_repository.delete_book(book_id)
        ## the deletion is prevented for now, if a book has active loans or had active loans in the past
