from sqlalchemy.orm import Session
from sqlalchemy.future import select
from APP.domain.entities.Borrowers import Borrower
from APP.repositories.Interfaces.borrower_repository import BorrowerRepository
from uuid import UUID
from typing import List
from APP.models.borrower_model import BorrowerModel
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
class BorrowerSQLRepository(BorrowerRepository):
    def __init__(self, session: Session):
        self.session = session

    async def get_borrowers(self) -> List[Borrower]:
        result = await self.session.execute(select(BorrowerModel))
        borrowers = result.scalars().all()
        return [Borrower(
            id=b.id,
            name=b.name,
            email=b.email,
            phone=b.phone,
            created_at=b.created_at,
            updated_at=b.updated_at
        ) for b in borrowers]
    
    async def create_borrower(self, borrower: Borrower) -> Borrower:
        db_borrower = BorrowerModel(
            id=borrower.id,
            name=borrower.name,
            email=borrower.email,
            phone=borrower.phone,
            created_at=borrower.created_at,
            updated_at=borrower.updated_at
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
            updated_at=db_borrower.updated_at
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
            updated_at=db_borrower.updated_at
        )
    
    async def get_borrower_details(self, borrower_id: UUID) -> Borrower:
        b = await self.session.get(BorrowerModel, borrower_id)
        if b is None:
            return None
        return Borrower(
            id=b.id,
            name=b.name,
            email=b.email,
            phone=b.phone,
            created_at=b.created_at,
            updated_at=b.updated_at
        )
        
