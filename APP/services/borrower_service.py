from typing import List
from uuid import UUID

from APP.core.events import dispatch_event
from APP.domain.entities.Borrowers import Borrower
from APP.domain.events.domain_events import BorrowerCreated, BorrowerUpdated
from APP.domain.exceptions import BorrowerNotFoundError, EmailAlreadyInUseError
from APP.repositories.Interfaces.borrower_repository import BorrowerRepository


class BorrowerService:
    """
    Service layer for managing borrower-related business logic.
    """

    def __init__(self, repository: BorrowerRepository):
        self.repository = repository

    async def get_borrowers(self) -> List[Borrower]:
        """
        Retrieve all borrowers from the repository.
        """
        return await self.repository.get_borrowers()

    async def create_borrower(self, borrower: Borrower) -> Borrower:
        """
        Create a new borrower record, ensuring the email is unique.
        """
        email_exists = await self.repository.get_borrower_by_email(borrower.email)
        if email_exists:
            raise EmailAlreadyInUseError(borrower.email)
        created_borrower = await self.repository.create_borrower(borrower)
        dispatch_event(
            BorrowerCreated(
                borrower_id=created_borrower.id,
                data={
                    "name": created_borrower.name,
                    "email": created_borrower.email,
                    "phone": created_borrower.phone,
                },
            )
        )
        return created_borrower

    async def update_borrower(self, borrower_id: UUID, borrower: Borrower) -> Borrower:
        """
        Update an existing borrower's details, ensuring the email remains unique.
        """
        email_exists = await self.repository.get_borrower_by_email(borrower.email)
        if email_exists and email_exists.id != borrower_id:
            raise EmailAlreadyInUseError(borrower.email)
        updated_borrower = await self.repository.update_borrower(borrower_id, borrower)
        dispatch_event(
            BorrowerUpdated(
                borrower_id=updated_borrower.id,
                data={
                    "name": updated_borrower.name,
                    "email": updated_borrower.email,
                    "phone": updated_borrower.phone,
                },
            )
        )
        return updated_borrower

    async def get_borrower_details(self, borrower_id: UUID) -> Borrower:
        """
        Retrieve details for a specific borrower by their ID.
        """
        borrower = await self.repository.get_borrower_details(borrower_id)
        if not borrower:
            raise BorrowerNotFoundError(borrower_id)
        return borrower
