from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from APP.domain.entities.Loans import Loan


class LoansRepository(ABC):
    @abstractmethod
    async def create_loan(self, loan: Loan) -> Loan:
        pass

    @abstractmethod
    async def get_loans(self) -> List[Loan]:
        pass

    @abstractmethod
    async def get_loans_for_borrower(self, borrower_id: UUID) -> List[Loan]:
        pass

    @abstractmethod
    async def get_active_loans(self) -> List[Loan]:
        pass

    @abstractmethod
    async def set_returned(self, loan_id: UUID) -> Loan:
        pass
