from typing import Any, Dict
from uuid import UUID
from APP.domain.events.base import DomainEvent

class AuthorCreated(DomainEvent):
    def __init__(self, author_id: UUID, data: Dict[str, Any]):
        super().__init__(
            event_type="author.created",
            aggregate_type="author",
            aggregate_id=author_id,
            data=data
        )

class AuthorUpdated(DomainEvent):
    def __init__(self, author_id: UUID, data: Dict[str, Any]):
        super().__init__(
            event_type="author.updated",
            aggregate_type="author",
            aggregate_id=author_id,
            data=data
        )

class AuthorDeleted(DomainEvent):
    def __init__(self, author_id: UUID, data: Dict[str, Any]):
        super().__init__(
            event_type="author.deleted",
            aggregate_type="author",
            aggregate_id=author_id,
            data=data
        )

class BookCreated(DomainEvent):
    def __init__(self, book_id: UUID, data: Dict[str, Any]):
        super().__init__(
            event_type="book.created",
            aggregate_type="book",
            aggregate_id=book_id,
            data=data
        )

class BookUpdated(DomainEvent):
    def __init__(self, book_id: UUID, data: Dict[str, Any]):
        super().__init__(
            event_type="book.updated",
            aggregate_type="book",
            aggregate_id=book_id,
            data=data
        )

class BookDeleted(DomainEvent):
    def __init__(self, book_id: UUID, data: Dict[str, Any]):
        super().__init__(
            event_type="book.deleted",
            aggregate_type="book",
            aggregate_id=book_id,
            data=data
        )

class BorrowerCreated(DomainEvent):
    def __init__(self, borrower_id: UUID, data: Dict[str, Any]):
        super().__init__(
            event_type="borrower.created",
            aggregate_type="borrower",
            aggregate_id=borrower_id,
            data=data
        )

class BorrowerUpdated(DomainEvent):
    def __init__(self, borrower_id: UUID, data: Dict[str, Any]):
        super().__init__(
            event_type="borrower.updated",
            aggregate_type="borrower",
            aggregate_id=borrower_id,
            data=data
        )

class LoanCreated(DomainEvent):
    def __init__(self, loan_id: UUID, data: Dict[str, Any]):
        super().__init__(
            event_type="loan.created",
            aggregate_type="loan",
            aggregate_id=loan_id,
            data=data
        )

class LoanReturned(DomainEvent):
    def __init__(self, loan_id: UUID, data: Dict[str, Any]):
        super().__init__(
            event_type="loan.returned",
            aggregate_type="loan",
            aggregate_id=loan_id,
            data=data
        )
