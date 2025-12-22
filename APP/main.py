from fastapi import APIRouter, FastAPI
from APP.api import author
from APP.api import book
from APP.api import borrower
from APP.api import loans
from APP.core.database import engine, Base
import asyncio

router = APIRouter()

APP = FastAPI(title="Library API")
APP.include_router(author.router, tags=["Authors"])
APP.include_router(book.router,tags=["Books"])
APP.include_router(borrower.router,tags=["Borrowers"])
APP.include_router(loans.router,tags=["Loans"])