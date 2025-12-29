from fastapi import Request, status
from fastapi.responses import JSONResponse

from APP.domain.exceptions import (
    AuthorDeletionError,
    AuthorNotFoundError,
    BookAlreadyLoanedError,
    BookDeletionError,
    BookNotFoundError,
    BorrowerNotFoundError,
    EmailAlreadyInUseError,
    ISBNAlreadyExistsError,
    LoanAlreadyReturnedError,
    LoanNotFoundError,
)


async def book_not_found_exception_handler(request: Request, exc: BookNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def borrower_not_found_exception_handler(
    request: Request, exc: BorrowerNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def author_not_found_exception_handler(
    request: Request, exc: AuthorNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def book_already_loaned_exception_handler(
    request: Request, exc: BookAlreadyLoanedError
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


async def email_already_in_use_exception_handler(
    request: Request, exc: EmailAlreadyInUseError
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


async def author_deletion_exception_handler(request: Request, exc: AuthorDeletionError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def book_deletion_exception_handler(request: Request, exc: BookDeletionError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def loan_not_found_exception_handler(request: Request, exc: LoanNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def loan_already_returned_exception_handler(
    request: Request, exc: LoanAlreadyReturnedError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def isbn_already_exists_exception_handler(
    request: Request, exc: ISBNAlreadyExistsError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


def register_exception_handlers(app):
    app.add_exception_handler(BookNotFoundError, book_not_found_exception_handler)
    app.add_exception_handler(
        BorrowerNotFoundError, borrower_not_found_exception_handler
    )
    app.add_exception_handler(AuthorNotFoundError, author_not_found_exception_handler)
    app.add_exception_handler(
        BookAlreadyLoanedError, book_already_loaned_exception_handler
    )
    app.add_exception_handler(
        EmailAlreadyInUseError, email_already_in_use_exception_handler
    )
    app.add_exception_handler(AuthorDeletionError, author_deletion_exception_handler)
    app.add_exception_handler(BookDeletionError, book_deletion_exception_handler)
    app.add_exception_handler(LoanNotFoundError, loan_not_found_exception_handler)
    app.add_exception_handler(
        LoanAlreadyReturnedError, loan_already_returned_exception_handler
    )
    app.add_exception_handler(
        ISBNAlreadyExistsError, isbn_already_exists_exception_handler
    )
