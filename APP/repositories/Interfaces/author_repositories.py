from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from APP.domain.entities.author import Author


class AuthorRepository(ABC):

    @abstractmethod
    async def get_authors(self) -> List[Author]:
        pass

    @abstractmethod
    async def get_author_details(self, author_id: UUID) -> Author:
        pass

    @abstractmethod
    async def create_author(self, author: Author) -> Author:
        pass

    @abstractmethod
    async def update_author(self, author_id: UUID, author: Author) -> Author:
        pass

    @abstractmethod
    async def delete_author(self, author_id: UUID) -> None:
        pass
