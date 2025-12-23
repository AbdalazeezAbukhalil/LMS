from fastapi import FastAPI, Depends, Request
from fastapi.openapi.utils import get_openapi
from APP.api import author
from APP.api import book
from APP.api import borrower
from APP.api import loans
from APP.api import auth
from APP.core.security.dependencies import verify_jwt, verify_api_key
import asyncio

APP = FastAPI(title="Library API")

APP.include_router(auth.router, tags=["Auth"])

# api key and jwt applied
APP.include_router(
    author.router,
    tags=["Authors"],
    dependencies=[Depends(verify_jwt), Depends(verify_api_key)],
)
APP.include_router(
    book.router,
    tags=["Books"],
    dependencies=[Depends(verify_jwt), Depends(verify_api_key)],
)
APP.include_router(
    borrower.router,
    tags=["Borrowers"],
    dependencies=[Depends(verify_jwt), Depends(verify_api_key)],
)
APP.include_router(
    loans.router,
    tags=["Loans"],
    dependencies=[Depends(verify_jwt), Depends(verify_api_key)],
)
