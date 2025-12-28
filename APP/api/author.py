from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException

from APP.core.dependency_injection import get_author_service
from APP.core.security.dependencies import get_current_user
from APP.domain.entities.author import Author
from APP.models.user_model import UserModel
from APP.schemas.author_schemas import (
    AuthorCreateSchema,
    AuthorReadSchema,
    AuthorUpdateSchema,
    AuthorWithBooksSchema,
)
from APP.services.author_service import AuthorService

router = APIRouter()


@router.get("/authors", response_model=List[AuthorWithBooksSchema])
async def get_authors(
    service: AuthorService = Depends(get_author_service),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Retrieve a list of all authors with their associated books.
    """
    return await service.get_authors()


@router.get("/authors/{author_id}", response_model=AuthorWithBooksSchema)
async def get_author_details(
    author_id: UUID,
    service: AuthorService = Depends(get_author_service),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Retrieve detailed information about a specific author, including their books.
    """
    author_details = await service.get_author_details(author_id)
    if not author_details:
        raise HTTPException(status_code=404, detail="Author not found")
    return author_details


@router.post("/authors", response_model=AuthorReadSchema)
async def create_author(
    author: AuthorCreateSchema,
    service: AuthorService = Depends(get_author_service),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Create a new author record.
    """
    entity = Author(
        id=uuid4(),
        name=author.name,
        bio=author.bio,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    return await service.create_author(entity)


@router.put("/authors/{author_id}", response_model=AuthorReadSchema)
async def update_author(
    author_id: UUID,
    author: AuthorUpdateSchema,
    service: AuthorService = Depends(get_author_service),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Update an existing author's information.
    """
    author_details = await service.get_author_details(author_id)
    if not author_details:
        raise HTTPException(status_code=404, detail="Author not found")
    entity = Author(
        id=author_id,
        name=author.name,
        bio=author.bio,
        created_at=datetime.utcnow(),  # or fetch original created_at
        updated_at=datetime.utcnow(),
    )
    return await service.update_author(author_id, entity)


@router.delete("/authors/{author_id}", response_model=None)
async def delete_author(
    author_id: UUID,
    service: AuthorService = Depends(get_author_service),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Delete an author record.
    """
    author_details = await service.get_author_details(author_id)
    if not author_details:
        raise HTTPException(status_code=404, detail="Author not found")
    return await service.delete_author(author_id)
