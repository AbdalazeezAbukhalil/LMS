from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from APP.domain.entities.books import Book


class BookRepository(ABC):

    @abstractmethod
    async def get_books(self) -> List[Book]:
        pass

    @abstractmethod
    async def get_book_details(self, book_id: UUID) -> Book:
        pass

    @abstractmethod
    async def create_book(self, book: Book) -> Book:
        pass

    @abstractmethod
    async def update_book(self, book_id: UUID, book: Book) -> Book:
        pass

    @abstractmethod
    async def delete_book(self, book_id: UUID) -> None:
        pass
