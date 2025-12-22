# APP/core/dependency_injection.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from APP.services.author_service import AuthorService
from APP.repositories.sqlalchemy.author_sqlRepository import AuthorSQLRepository
from APP.core.database import get_db  

from APP.services.book_service import BookService
from APP.repositories.sqlalchemy.book_sqlRepository import BookSQLRepository

from APP.services.borrower_service import BorrowerService
from APP.repositories.sqlalchemy.borrower_sqlRepository import BorrowerSQLRepository


from APP.services.loans_service import LoanService
from APP.repositories.sqlalchemy.loans_sqlRepository import LoansSQLRepository

async def get_author_service(session: AsyncSession = Depends(get_db)) -> AuthorService:
    repo = AuthorSQLRepository(session)
    service = AuthorService(repo)
    return service

async def get_book_service(session: AsyncSession = Depends(get_db), author_service: AuthorService = Depends(get_author_service)) -> BookService:
    repo = BookSQLRepository(session)
    service = BookService(repo, author_service)
    return service

async def get_borrower_service(session: AsyncSession = Depends(get_db)) -> BorrowerService:
    repo = BorrowerSQLRepository(session)
    service = BorrowerService(repo)
    return service

async def get_loan_service(session: AsyncSession = Depends(get_db), book_service: BookService = Depends(get_book_service), borrower_service: BorrowerService = Depends(get_borrower_service)) -> LoanService:
    repo = LoansSQLRepository(session)
    service = LoanService(repo, book_service, borrower_service)
    return service