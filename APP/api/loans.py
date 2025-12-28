from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException

from APP.core.dependency_injection import get_loan_service
from APP.core.security.dependencies import get_current_user, verify_jwt
from APP.domain.entities.Loans import Loan
from APP.models.user_model import UserModel
from APP.schemas.loans_schemas import LoanCreateSchema, LoanReadSchema
from APP.services.book_service import BookService
from APP.services.borrower_service import BorrowerService
from APP.services.loans_service import LoanService

router = APIRouter()


@router.get("/loans/", response_model=List[LoanReadSchema])
async def get_loans(
    service: LoanService = Depends(get_loan_service),
    current_user: UserModel = Depends(get_current_user),
) -> List[Loan]:
    """
    Retrieve a list of all active and past loans.
    """
    return await service.get_loans()


@router.get("/loans/active", response_model=List[LoanReadSchema])
async def get_active_loans(
    service: LoanService = Depends(get_loan_service),
    current_user: UserModel = Depends(get_current_user),
) -> List[Loan]:
    """
    Retrieve a list of all active (not returned) loans.
    """
    return await service.get_active_loans()


@router.post("/loans/create", response_model=LoanReadSchema)
async def create_loan(
    loan: LoanCreateSchema,
    service: LoanService = Depends(get_loan_service),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Create a new loan record (borrow a book).
    """
    entity = Loan(
        id=uuid4(),
        book_id=loan.book_id,
        borrower_id=loan.borrower_id,
        loan_date=datetime.utcnow(),
        return_date=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    return await service.create_loan(entity)


@router.get(
    "/loans/history/borrower/{borrower_id}", response_model=List[LoanReadSchema]
)
async def get_loans_history_for_borrower(
    borrower_id: UUID, service: LoanService = Depends(get_loan_service)
):
    """
    Retrieve the loan history for a specific borrower.
    """
    loans = await service.get_loans_for_borrower(borrower_id)  # returns List[Loan]
    if not loans:
        raise HTTPException(status_code=404, detail="No loans found for this borrower")

    return [
        LoanReadSchema(
            id=loan.id,
            book_id=loan.book_id,
            borrower_id=loan.borrower_id,
            loan_date=loan.loan_date,
            return_date=loan.return_date,
            created_at=loan.created_at,
            updated_at=loan.updated_at,
        )
        for loan in loans
    ]


@router.put("/loans/return/{id}", response_model=LoanReadSchema)
async def set_returned_date(id: UUID, service: LoanService = Depends(get_loan_service)):
    
    """
    Mark a loan as returned by setting the return date to now.
    """
    return await service.set_returned(id)
