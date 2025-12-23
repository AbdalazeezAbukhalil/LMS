from fastapi import APIRouter, Depends
from typing import List
from uuid import uuid4, UUID
from datetime import datetime

from fastapi import HTTPException
from APP.services.author_service import AuthorService
from APP.core.dependency_injection import get_book_service
from APP.schemas.book_schema import BookCreateSchema, BookUpdateSchema, BookReadSchema
from APP.domain.entities.books import Book
from APP.services.book_service import BookService
from APP.core.security.dependencies import verify_jwt, get_current_user
from APP.models.user_model import UserModel

router = APIRouter()


@router.get("/books", response_model=List[BookReadSchema])
async def get_books(
    service: BookService = Depends(get_book_service),
    current_user: UserModel = Depends(get_current_user),
):
    return await service.get_books()


@router.get("/books/{book_id}", response_model=BookReadSchema)
async def get_book_details(
    book_id: UUID,
    service: BookService = Depends(get_book_service),
    current_user: UserModel = Depends(get_current_user),
):
    book_details = await service.get_book_details(book_id)
    if not book_details:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_details


@router.post("/books", response_model=BookReadSchema)
async def create_book(
    book: BookCreateSchema,
    service: BookService = Depends(get_book_service),
    current_user: UserModel = Depends(get_current_user),
):
    entity = Book(
        id=uuid4(),
        title=book.title,
        ISBN=book.ISBN,
        published_date=datetime.utcnow(),
        author_id=book.author_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    return await service.create_book(entity)


@router.put("/books/{book_id}", response_model=BookReadSchema)
async def update_book(
    book_id: UUID,
    book: BookUpdateSchema,
    service: BookService = Depends(get_book_service),
    current_user: UserModel = Depends(get_current_user),
):
    book_details = await service.get_book_details(book_id)
    if not book_details:
        raise HTTPException(status_code=404, detail="Book not found")
    entity = Book(
        id=book_id,
        title=book.title,
        ISBN=book.ISBN,
        published_date=datetime.utcnow(),
        author_id=book.author_id,
        created_at=datetime.utcnow(),  # everytime we uopdate a book, we set created_at to now
        updated_at=datetime.utcnow(),  # same as above
    )
    return await service.update_book(book_id, entity)


@router.delete("/books/{book_id}", response_model=None)
async def delete_book(
    book_id: UUID,
    service: BookService = Depends(get_book_service),
    current_user: UserModel = Depends(get_current_user),
):
    book_details = await service.get_book_details(book_id)
    if not book_details:
        raise HTTPException(status_code=404, detail="Book not found")
    return await service.delete_book(book_id)
