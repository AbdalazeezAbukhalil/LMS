from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload

from APP.domain.entities.Borrowers import Borrower
from APP.domain.entities.Loans import Loan
from APP.models.borrower_model import BorrowerModel
from APP.repositories.Interfaces.borrower_repository import BorrowerRepository


class BorrowerSQLRepository(BorrowerRepository):
    def __init__(self, session: Session):
        self.session = session

    async def get_borrowers(self) -> List[Borrower]:
        result = await self.session.execute(
            select(BorrowerModel).options(selectinload(BorrowerModel.loans))
        )
        borrowers = result.scalars().all()
        return [
            Borrower(
                id=b.id,
                name=b.name,
                email=b.email,
                phone=b.phone,
                created_at=b.created_at,
                updated_at=b.updated_at,
                loans=[
                    Loan(
                        id=loan.id,
                        book_id=loan.book_id,
                        borrower_id=loan.borrower_id,
                        loan_date=loan.loan_date,
                        return_date=loan.return_date,
                        created_at=loan.created_at,
                        updated_at=loan.updated_at,
                    )
                    for loan in b.loans
                ],
            )
            for b in borrowers
        ]

    async def create_borrower(self, borrower: Borrower) -> Borrower:
        db_borrower = BorrowerModel(
            id=borrower.id,
            name=borrower.name,
            email=borrower.email,
            phone=borrower.phone,
            created_at=borrower.created_at,
            updated_at=borrower.updated_at,
        )
        self.session.add(db_borrower)
        try:
            await self.session.commit()
            await self.session.refresh(db_borrower)
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Email already exists")

        return Borrower(
            id=db_borrower.id,
            name=db_borrower.name,
            email=db_borrower.email,
            phone=db_borrower.phone,
            created_at=db_borrower.created_at,
            updated_at=db_borrower.updated_at,
        )

    async def update_borrower(self, borrower_id: UUID, borrower: Borrower) -> Borrower:
        db_borrower = await self.session.get(BorrowerModel, borrower_id)
        db_borrower.name = borrower.name
        db_borrower.email = borrower.email
        db_borrower.phone = borrower.phone
        self.session.add(db_borrower)
        try:
            await self.session.commit()
            await self.session.refresh(db_borrower)
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Email already exists")

        return Borrower(
            id=db_borrower.id,
            name=db_borrower.name,
            email=db_borrower.email,
            phone=db_borrower.phone,
            created_at=db_borrower.created_at,
            updated_at=db_borrower.updated_at,
        )

    async def get_borrower_details(self, borrower_id: UUID) -> Borrower:
        stmt = (
            select(BorrowerModel)
            .where(BorrowerModel.id == borrower_id)
            .options(selectinload(BorrowerModel.loans))
        )
        result = await self.session.execute(stmt)
        b = result.scalar_one_or_none()

        if b is None:
            return None
        return Borrower(
            id=b.id,
            name=b.name,
            email=b.email,
            phone=b.phone,
            created_at=b.created_at,
            updated_at=b.updated_at,
            loans=[
                Loan(
                    id=loan.id,
                    book_id=loan.book_id,
                    borrower_id=loan.borrower_id,
                    loan_date=loan.loan_date,
                    return_date=loan.return_date,
                    created_at=loan.created_at,
                    updated_at=loan.updated_at,
                )
                for loan in b.loans
            ],
        )

    async def get_borrower_by_email(self, email: str) -> Optional[BorrowerModel]:
        stmt = select(BorrowerModel).where(BorrowerModel.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
