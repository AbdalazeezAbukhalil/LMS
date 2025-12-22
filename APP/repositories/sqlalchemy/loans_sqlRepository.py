from sqlalchemy.orm import Session
from sqlalchemy.future import select
from APP.domain.entities.Loans import Loan
from APP.repositories.Interfaces.loans_repository import LoansRepository
from uuid import UUID
from typing import List
from APP.models.loans_model import LoanModel
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime

class LoansSQLRepository(LoansRepository):
    def __init__(self, session: Session):
        self.session = session

    async def create_loan(self, loan: Loan) -> Loan:
        db_loan = LoanModel(
            id=loan.id,
            book_id=loan.book_id,
            borrower_id=loan.borrower_id,
            loan_date=loan.loan_date,
            return_date=loan.return_date,
            created_at=loan.created_at,
            updated_at=loan.updated_at
        )
        self.session.add(db_loan)
        await self.session.commit()
        await self.session.refresh(db_loan)
        return Loan(
            id=db_loan.id,
            book_id=db_loan.book_id,
            borrower_id=db_loan.borrower_id,
            loan_date=db_loan.loan_date,
            return_date=db_loan.return_date,
            created_at=db_loan.created_at,
            updated_at=db_loan.updated_at
        )

    async def get_loans(self) -> List[Loan]:
        result = await self.session.execute(select(LoanModel))
        loans = result.scalars().all()
        return [Loan(
            id=l.id,
            book_id=l.book_id,
            borrower_id=l.borrower_id,
            loan_date=l.loan_date,
            return_date=l.return_date,
            returned=l.returned,
            created_at=l.created_at,
            updated_at=l.updated_at
        ) for l in loans]

    async def get_loans_for_borrower(self, borrower_id: UUID) -> List[Loan]:
        result = await self.session.execute(
            select(LoanModel).where(LoanModel.borrower_id == borrower_id)
        )
        loans = result.scalars().all()
        return [Loan(
            id=l.id,
            book_id=l.book_id,
            borrower_id=l.borrower_id,
            loan_date=l.loan_date,
            return_date=l.return_date,
            returned=l.returned,
            created_at=l.created_at,
            updated_at=l.updated_at
        ) for l in loans]

    async def set_returned(self, loan_id: UUID) -> Loan:
        db_loan = await self.session.get(LoanModel, loan_id)
        if db_loan is None:
            raise HTTPException(status_code=404, detail="Loan not found")
        db_loan.return_date = datetime.utcnow()
        self.session.add(db_loan)
        await self.session.commit()
        await self.session.refresh(db_loan)
        return Loans(
            id=db_loan.id,
            book_id=db_loan.book_id,
            borrower_id=db_loan.borrower_id,
            loan_date=db_loan.loan_date,
            return_date=db_loan.return_date,
            returned=db_loan.returned,
            created_at=db_loan.created_at,
            updated_at=db_loan.updated_at
        )
    async def has_active_loan_for_book(self, book_id: UUID) -> bool:
        stmt = select(LoanModel).where(
            LoanModel.book_id == book_id,
            LoanModel.return_date.is_(None)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None    