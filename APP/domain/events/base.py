from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    aggregate_type: str
    aggregate_id: UUID
    data: Dict[str, Any]
