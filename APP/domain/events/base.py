from pydantic import BaseModel, Field
from datetime import datetime

from typing import Any, Dict
from uuid import UUID, uuid4


class DomainEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    aggregate_type: str
    aggregate_id: UUID
    data: Dict[str, Any]
