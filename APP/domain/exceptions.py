import uuid


class BookNotFoundError(Exception):
    def __init__(self, book_id: uuid.UUID):
        self.book_id = book_id
        super().__init__(f"Book with id {book_id} was not found")


class BorrowerNotFoundError(Exception):
    def __init__(self, borrower_id: uuid.UUID):
        self.borrower_id = borrower_id
        super().__init__(f"Borrower with id {borrower_id} was not found")


class AuthorNotFoundError(Exception):
    def __init__(self, author_id: uuid.UUID):
        self.author_id = author_id
        super().__init__(f"Author with id {author_id} was not found")


class BookAlreadyLoanedError(Exception):
    def __init__(self, book_id: uuid.UUID):
        self.book_id = book_id
        super().__init__(f"Book with id {book_id} already has an active loan")


class EmailAlreadyInUseError(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email {email} is already in use")


class AuthorDeletionError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class BookDeletionError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class LoanNotFoundError(Exception):
    def __init__(self, loan_id: uuid.UUID):
        self.loan_id = loan_id
        super().__init__(f"Loan with id {loan_id} was not found")


class LoanAlreadyReturnedError(Exception):
    def __init__(self, loan_id: uuid.UUID):
        self.loan_id = loan_id
        super().__init__(f"Loan with id {loan_id} is already returned")


class ISBNAlreadyExistsError(Exception):
    def __init__(self, isbn: str):
        self.isbn = isbn
        super().__init__(f"Book with ISBN {isbn} already exists")
