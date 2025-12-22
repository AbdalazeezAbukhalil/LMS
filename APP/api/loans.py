from fastapi import APIRouter, Depends
from typing import List
from uuid import uuid4, UUID
from datetime import datetime

from fastapi import HTTPException
from APP.services.book_service import BookService
from APP.services.borrower_service import BorrowerService
from APP.core.dependency_injection import get_loan_service
from APP.schemas.loans_schemas import LoanCreateSchema, LoanReadSchema
from APP.domain.entities.Loans import Loan
from APP.services.loans_service import LoanService

router = APIRouter()

@router.get("/loans/", response_model=List[LoanReadSchema])
async def get_loans(service: LoanService = Depends(get_loan_service)) -> List[Loan]:
    return await service.get_loans()
@router.post("/loans", response_model=LoanReadSchema)
async def create_loan(loan: LoanCreateSchema, service: LoanService = Depends(get_loan_service)):
    entity = Loan(
        id=uuid4(),
        book_id=loan.book_id,
        borrower_id=loan.borrower_id,
        loan_date=datetime.utcnow(),
        return_date=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return await service.create_loan(entity)

@router.get("/loans/{borrower_id}", response_model=List[LoanReadSchema])
async def get_loans_history_for_borrower(
    borrower_id: UUID,
    service: LoanService = Depends(get_loan_service)
):
    loans = await service.get_loans_for_borrower(borrower_id)  # returns List[Loan]
    if not loans:
        raise HTTPException(status_code=404, detail="No loans found for this borrower")

    return [
        LoanReadSchema(
            id=l.id,
            book_id=l.book_id,
            borrower_id=l.borrower_id,
            loan_date=l.loan_date,
            return_date=l.return_date,
            created_at=l.created_at,
            updated_at=l.updated_at
        )
        for l in loans
    ]

@router.put("/loans/{id}", response_model=LoanReadSchema)
async def set_returned_date(id: UUID, service: LoanService = Depends(get_loan_service)):
    return await service.set_returned(id)