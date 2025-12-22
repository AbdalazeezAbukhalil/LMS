from typing import List
from uuid import UUID
from fastapi import HTTPException
from APP.domain.entities.Loans import Loan
from APP.repositories.Interfaces.loans_repository import LoansRepository
from APP.services.book_service import BookService
from APP.services.borrower_service import BorrowerService


class LoanService:
    def __init__(self, loans_repository: LoansRepository, book_service: BookService, borrower_service: BorrowerService):
        self.loans_repository = loans_repository
        self.book_service = book_service
        self.borrower_service = borrower_service
    
    async def get_loans(self) -> List[Loan]:
        return await self.loans_repository.get_loans()
    async def create_loan(self, loan: Loan) -> Loan:
        # Check if book exists
        book = await self.book_service.get_book_details(loan.book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        borrower = await self.borrower_service.get_borrower_details(loan.borrower_id)         # Check if borrower exists
        if not borrower:
            raise HTTPException(status_code=404, detail="Borrower not found")

        if await self.loans_repository.has_active_loan_for_book(loan.book_id): # cehck if the book is loaned (active)
            raise HTTPException(
                status_code=409,
                detail="This book already has an active loan",
            )
        return await self.loans_repository.create_loan(loan)
    
    async def get_loans_for_borrower(self, borrower_id: UUID) -> List[Loan]:
        return await self.loans_repository.get_loans_for_borrower(borrower_id)
    async def set_returned(self, loan_id: UUID) -> Loan:
        return await self.loans_repository.set_returned(loan_id)