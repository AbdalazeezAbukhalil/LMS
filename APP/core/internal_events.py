from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class InternalEvent(BaseModel):
    """
    Base class for all required internal technical/workflow signals.
    """

    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    component: str
    data: Dict[str, Any] = Field(default_factory=dict)


class ValidationFailed(InternalEvent):
    """
    for now it is used only for loans validation failures, it can be extended later
    """

    def __init__(self, component: str, data: Dict[str, Any]):
        super().__init__(
            event_type=f"{component.lower()}.validation_failed",
            component=component,
            data=data,
        )


class AuthFailed(InternalEvent):
    """
    Event triggered when an authentication failure occurs like invalid credentials or wrong api ke
    """

    def __init__(self, component: str, reason: str, data: Dict[str, Any]):
        data["reason"] = reason
        super().__init__(
            event_type="security.auth_failed", component=component, data=data
        )
