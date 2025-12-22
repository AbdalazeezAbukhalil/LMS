# APP/services/author_service.py
from typing import List
from uuid import UUID
from APP.domain.entities.author import Author
from APP.repositories.Interfaces.author_repositories import AuthorRepository

class AuthorService:
    def __init__(self, author_repository: AuthorRepository):
        self.author_repository = author_repository

    async def get_authors(self) -> List[Author]:
        return await self.author_repository.get_authors()

    async def get_author_details(self, author_id: UUID) -> Author:
        return await self.author_repository.get_author_details(author_id)

    async def create_author(self, author: Author) -> Author:
        return await self.author_repository.create_author(author)

    async def update_author(self, author_id: UUID, author: Author) -> Author:
        return await self.author_repository.update_author(author_id, author)

    async def delete_author(self, author_id: UUID) -> None:
        return await self.author_repository.delete_author(author_id)
