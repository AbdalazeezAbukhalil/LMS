from typing import List
from uuid import UUID

from APP.domain.entities.Loans import Loan
from APP.domain.exceptions import (
    BookAlreadyLoanedError,
    BookNotFoundError,
    BorrowerNotFoundError,
)
from APP.repositories.Interfaces.loans_repository import LoansRepository
from APP.schemas.loans_schemas import LoanReadSchema
from APP.services.book_service import BookService
from APP.services.borrower_service import BorrowerService


class LoanService:
    """
    Service layer for managing loan-related business logic.
    """

    def __init__(
        self,
        loans_repository: LoansRepository,
        book_service: BookService,
        borrower_service: BorrowerService,
    ):
        self.loans_repository = loans_repository
        self.book_service = book_service
        self.borrower_service = borrower_service

    async def get_loans(self) -> List[Loan]:
        """
        Retrieve all loans from the repository.
        """
        return await self.loans_repository.get_loans()

    async def get_active_loans(self) -> List[Loan]:
        """
        Retrieve all active (not returned) loans from the repository.
        """
        return await self.loans_repository.get_active_loans()

    async def create_loan(self, loan: Loan) -> Loan:
        """
        Create a new loan record, ensuring the book and borrower exist and the book is available.
        """
        # Check if book exists
        book = await self.book_service.get_book_details(loan.book_id)
        if not book:
            raise BookNotFoundError(loan.book_id)

        borrower = await self.borrower_service.get_borrower_details(
            loan.borrower_id
        )  # Check if borrower exists
        if not borrower:
            raise BorrowerNotFoundError(loan.borrower_id)

        if await self.loans_repository.has_active_loan_for_book(
            loan.book_id
        ):  # cehck if the book is loaned (active)
            raise BookAlreadyLoanedError(loan.book_id)
        return await self.loans_repository.create_loan(loan)

    async def get_loans_for_borrower(self, borrower_id: UUID) -> List[Loan]:
        """
        Retrieve all loans associated with a specific borrower.
        """
        return await self.loans_repository.get_loans_for_borrower(borrower_id)

    async def set_returned(self, loan_id: UUID) -> LoanReadSchema:
        return await self.loans_repository.set_returned(loan_id)
