from fastapi import APIRouter, Depends
from typing import List
from uuid import uuid4, UUID
from datetime import datetime

from fastapi import HTTPException
from APP.services.book_service import BookService
from APP.services.borrower_service import BorrowerService
from APP.core.dependency_injection import get_loan_service
from APP.schemas.loans_schemas import LoanCreateSchema, LoanUpdateSchema, LoanReadSchema
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

@router.get("/loans/{id}", response_model=LoanReadSchema)
async def get_loans_for_borrower(id: UUID, service: LoanService = Depends(get_loan_service)):
    loan_details = await service.get_loan_details(id)
    if not loan_details:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan_details

@router.put("/loans/{id}", response_model=LoanReadSchema)
async def set_returned_date(id: UUID, loan: LoanUpdateSchema, service: LoanService = Depends(get_loan_service)):
    loan_details = await service.get_loan_details(id)
    if not loan_details:
        raise HTTPException(status_code=404, detail="Loan not found")
    entity = Loans(
        id=id,
        book_id=loan_details.book_id,
        borrower_id=loan_details.borrower_id,
        loan_date=loan_details.loan_date,
        return_date=loan.return_date,
        created_at=loan_details.created_at,
        updated_at=datetime.utcnow()
    )
    return await service.update_loan(id, entity)