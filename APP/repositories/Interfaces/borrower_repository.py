from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from APP.domain.entities.Borrowers import Borrower

class BorrowerRepository(ABC):
    @abstractmethod
    async def get_borrowers(self) -> List[Borrower]:
        pass
    
    @abstractmethod
    async def create_borrower(self, borrower: Borrower) -> Borrower:
        pass
    
    @abstractmethod
    async def update_borrower(self, borrower_id: UUID, borrower: Borrower) -> Borrower:
        pass
    
    @abstractmethod
    async def get_borrower_details(self, borrower_id: UUID) -> Borrower:
        pass