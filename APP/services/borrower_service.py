from typing import List
from uuid import UUID
from fastapi import HTTPException
from APP.domain.entities.Borrowers import Borrower
from APP.repositories.Interfaces.borrower_repository import BorrowerRepository

class BorrowerService:
    def __init__(self, repository: BorrowerRepository):
        self.repository = repository

    async def get_borrowers(self) -> List[Borrower]:
        return await self.repository.get_borrowers()
    async def create_borrower(self, borrower: Borrower) -> Borrower:
        email_exists = await self.repository.get_borrower_by_email(borrower.email)
        if email_exists:
            raise HTTPException(status_code=409, detail="Email already in use")
        return await self.repository.create_borrower(borrower)
    async def update_borrower(self, borrower_id: UUID, borrower: Borrower) -> Borrower:
        email_exists = await self.repository.get_borrower_by_email(borrower.email)
        if email_exists and email_exists.id != borrower_id:
            raise HTTPException(status_code=409, detail="Email already in use")
        return await self.repository.update_borrower(borrower_id, borrower)

    async def get_borrower_details(self, borrower_id: UUID) -> Borrower:
        borrower = await self.repository.get_borrower_details(borrower_id)
        if not borrower:
            raise HTTPException(status_code=404, detail="Borrower not found")
        return borrower