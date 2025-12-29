import json
from APP.domain.events.base import DomainEvent

def dispatch_event(event: DomainEvent):
    """
    for now we just print the event
    """
    print(f"\n[DOMAIN EVENT RELEASED]")
    print(f"Event ID: {event.event_id}")
    print(f"Event Type: {event.event_type}")
    print(f"Occurred At: {event.occurred_at}")
    print(f"Aggregate: {event.aggregate_type} ({event.aggregate_id})")
    print(f"Data: {json.dumps(event.data, indent=2, default=str)}")
    print("-" * 30)
