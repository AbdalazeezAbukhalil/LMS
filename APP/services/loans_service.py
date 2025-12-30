from typing import List
from uuid import UUID

from APP.core.events import dispatch_event, dispatch_internal_event
from APP.core.internal_events import ValidationFailed
from APP.domain.entities.Loans import Loan
from APP.domain.events.domain_events import LoanCreated, LoanReturned
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
            await dispatch_internal_event(
                ValidationFailed(
                    component="Loan",
                    data={"reason": "Book not found", "book_id": str(loan.book_id)},
                )
            )
            raise BookNotFoundError(loan.book_id)

        # Check if borrower exists
        try:
            borrower = await self.borrower_service.get_borrower_details(
                loan.borrower_id
            )
        except BorrowerNotFoundError:
            await dispatch_internal_event(
                ValidationFailed(
                    component="Loan",
                    data={
                        "reason": "Borrower not found",
                        "borrower_id": str(loan.borrower_id),
                    },
                )
            )
            raise BorrowerNotFoundError(loan.borrower_id)

        if await self.loans_repository.has_active_loan_for_book(
            loan.book_id
        ):  # cehck if the book is loaned (active)
            await dispatch_internal_event(
                ValidationFailed(
                    component="Loan",
                    data={
                        "reason": "Book already has an active loan",
                        "book_id": str(loan.book_id),
                    },
                )
            )
            raise BookAlreadyLoanedError(loan.book_id)
        created_loan = await self.loans_repository.create_loan(loan)
        dispatch_event(
            LoanCreated(
                loan_id=created_loan.id,
                data={
                    "book_id": created_loan.book_id,
                    "borrower_id": created_loan.borrower_id,
                    "loan_date": created_loan.loan_date,
                },
            )
        )
        return created_loan

    async def get_loans_for_borrower(self, borrower_id: UUID) -> List[Loan]:
        """
        Retrieve all loans associated with a specific borrower. also validates borrower existence.
        """
        try:
            borrower = await self.borrower_service.get_borrower_details(borrower_id)
        except BorrowerNotFoundError:
            await dispatch_internal_event(
                ValidationFailed(
                    component="Loan",
                    data={
                        "reason": "Borrower not found",
                        "borrower_id": str(borrower_id),
                    },
                )
            )
            raise BorrowerNotFoundError(borrower_id)
        return await self.loans_repository.get_loans_for_borrower(borrower_id)

    async def set_returned(self, loan_id: UUID) -> LoanReadSchema:
        returned_loan = await self.loans_repository.set_returned(loan_id)
        dispatch_event(
            LoanReturned(
                loan_id=returned_loan.id,
                data={
                    "book_id": returned_loan.book_id,
                    "borrower_id": returned_loan.borrower_id,
                    "return_date": returned_loan.return_date,
                },
            )
        )
        return returned_loan
