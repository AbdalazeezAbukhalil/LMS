from fastapi import Depends, FastAPI

from APP.api import auth, author, book, borrower, loans
from APP.api.exception_handlers import register_exception_handlers
from APP.core.security.dependencies import verify_api_key, verify_jwt

APP = FastAPI(title="Library Management System")

register_exception_handlers(APP)

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
