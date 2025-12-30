import json
import asyncio
from APP.domain.events.base import DomainEvent
from APP.core.internal_events import InternalEvent
from APP.core.kafka import publish_to_kafka


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


async def _publish_internal_background(topic: str, event: InternalEvent):
    """
    Background task to publish internal events to Kafka.
    """
    try:
        await asyncio.wait_for(publish_to_kafka(topic, event.model_dump()), timeout=2.0)
        print(f"Successfully published to Kafka topic: {topic}")
    except Exception as e:
        print(f"Failed to publish internal event to Kafka: {e}")


async def dispatch_internal_event(event: InternalEvent):
    """
    Internal events are technical signals.
    We print them immediately and publish to Kafka in the background.
    """
    print(f"\n[INTERNAL EVENT SIGNALED]", flush=True)
    print(f"Event ID: {event.event_id}", flush=True)
    print(f"Event Type: {event.event_type}", flush=True)
    print(f"Component: {event.component}", flush=True)
    print(f"Data: {json.dumps(event.data, indent=2, default=str)}", flush=True)
    print("-" * 30, flush=True)

    topic = "lms.internal.events"
    asyncio.create_task(_publish_internal_background(topic, event))
    """
    for now kafka isn't up and running, so we just print the event, but we can consume it later
    """
