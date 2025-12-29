# APP/services/author_service.py
from typing import List
from uuid import UUID

from APP.core.events import dispatch_event
from APP.domain.entities.author import Author
from APP.domain.events.domain_events import (
    AuthorCreated,
    AuthorDeleted,
    AuthorUpdated,
)
from APP.domain.exceptions import AuthorDeletionError
from APP.repositories.Interfaces.author_repositories import AuthorRepository


class AuthorService:
    """
    Service layer for managing author-related business logic.
    """

    def __init__(self, author_repository: AuthorRepository):
        self.author_repository = author_repository

    async def get_authors(self) -> List[Author]:
        """
        Retrieve all authors from the repository.
        """
        return await self.author_repository.get_authors()

    async def get_author_details(self, author_id: UUID) -> Author:
        """
        Retrieve details for a specific author by their ID.
        """
        return await self.author_repository.get_author_details(author_id)

    async def create_author(self, author: Author) -> Author:
        """
        Create a new author record.
        """
        created_author = await self.author_repository.create_author(author)
        dispatch_event(
            AuthorCreated(
                author_id=created_author.id,
                data={"name": created_author.name, "bio": created_author.bio},
            )
        )
        return created_author

    async def update_author(self, author_id: UUID, author: Author) -> Author:
        """
        Update an existing author's details.
        """
        updated_author = await self.author_repository.update_author(author_id, author)
        dispatch_event(
            AuthorUpdated(
                author_id=updated_author.id,
                data={"name": updated_author.name, "bio": updated_author.bio},
            )
        )
        return updated_author

    async def delete_author(self, author_id: UUID) -> None:
        """
        Delete an author if they have no books or loan history.
        """
        if await self.author_repository.has_loans(author_id):
            raise AuthorDeletionError(
                "Cannot delete author because one of their books has/had a loan."
            )
        if await self.author_repository.has_books(author_id):
            raise AuthorDeletionError(
                "Cannot delete author because they have books in the library."
            )
        await self.author_repository.delete_author(author_id)
        dispatch_event(AuthorDeleted(author_id=author_id, data={}))
