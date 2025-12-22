from fastapi import FastAPI, APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID, uuid4
from APP.domain.entities.Borrowers import Borrower
from APP.services.borrower_service import BorrowerService
from APP.schemas.borrower_schemas import BorrowerCreateSchema, BorrowerUpdateSchema, BorrowerReadSchema
from APP.core.dependency_injection import get_borrower_service
from datetime import datetime

router = APIRouter()
@router.get("/borrowers/", response_model=List[BorrowerReadSchema])
async def get_borrowers(service: BorrowerService = Depends(get_borrower_service)) -> List[Borrower]:
    return await service.get_borrowers()

@router.post("/borrowers", response_model=BorrowerReadSchema)
async def create_borrower(borrower: BorrowerCreateSchema, service: BorrowerService = Depends(get_borrower_service)):
    entiry = Borrower(
        id=uuid4(),
        name=borrower.name,
        email=borrower.email,
        phone=borrower.phone,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return await service.create_borrower(entiry)

@router.put("/borrowers/{id}", response_model=BorrowerReadSchema)
async def update_borrower(id: UUID, borrower: BorrowerUpdateSchema, service: BorrowerService = Depends(get_borrower_service)):
    borrower_det = await service.get_borrower_details(id)
    if not borrower_det:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return await service.update_borrower(id, borrower)

@router.get("/borrowers/{id}", response_model=BorrowerReadSchema)
async def get_borrower_details(id: UUID, service: BorrowerService = Depends(get_borrower_service)):
    borrower_details = await service.get_borrower_details(id)
    if not borrower_details:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return borrower_details