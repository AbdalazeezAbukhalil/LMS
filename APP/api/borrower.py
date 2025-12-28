from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException

from APP.core.dependency_injection import get_borrower_service
from APP.core.security.dependencies import get_current_user
from APP.domain.entities.Borrowers import Borrower
from APP.models.user_model import UserModel
from APP.schemas.borrower_schemas import (
    BorrowerCreateSchema,
    BorrowerReadSchema,
    BorrowerUpdateSchema,
    BorrowerWithLoansSchema,
)
from APP.services.borrower_service import BorrowerService

router = APIRouter()


@router.get("/borrowers/", response_model=List[BorrowerWithLoansSchema])
async def get_borrowers(
    service: BorrowerService = Depends(get_borrower_service),
    current_user: UserModel = Depends(get_current_user),
) -> List[Borrower]:
    """
    Retrieve a list of all borrowers with their loan history.
    """
    return await service.get_borrowers()


@router.post("/borrowers", response_model=BorrowerReadSchema)
async def create_borrower(
    borrower: BorrowerCreateSchema,
    service: BorrowerService = Depends(get_borrower_service),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Register a new borrower.
    """
    entiry = Borrower(
        id=uuid4(),
        name=borrower.name,
        email=borrower.email,
        phone=borrower.phone,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    return await service.create_borrower(entiry)


@router.put("/borrowers/{id}", response_model=BorrowerReadSchema)
async def update_borrower(
    id: UUID,
    borrower: BorrowerUpdateSchema,
    service: BorrowerService = Depends(get_borrower_service),
):
    """
    Update a borrower's profile information.
    """
    borrower_det = await service.get_borrower_details(id)
    if not borrower_det:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return await service.update_borrower(id, borrower)


@router.get("/borrowers/{id}", response_model=BorrowerWithLoansSchema)
async def get_borrower_details(
    id: UUID, service: BorrowerService = Depends(get_borrower_service)
):
    """
    Retrieve detailed information about a specific borrower, including their loan history.
    """
    borrower_details = await service.get_borrower_details(id)
    if not borrower_details:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return borrower_details
