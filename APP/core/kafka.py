import json
import asyncio
from aiokafka import AIOKafkaProducer
from APP.core.config import settings


class KafkaProducerManager:
    _producer: AIOKafkaProducer = None

    @classmethod
    async def get_producer(cls) -> AIOKafkaProducer:
        if cls._producer is None:
            try:
                cls._producer = AIOKafkaProducer(
                    bootstrap_servers=settings.kafka_bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v, default=str).encode(
                        "utf-8"
                    ),
                    request_timeout_ms=1000,  # Fail fast
                    retry_backoff_ms=100,
                )
                await cls._producer.start()
            except Exception as e:
                cls._producer = None
                raise e
        return cls._producer

    @classmethod
    async def stop_producer(cls):
        if cls._producer:
            await cls._producer.stop()
            cls._producer = None


async def publish_to_kafka(topic: str, message: dict):
    """
    Helper function to publish a message to a Kafka topic.
    In a real app, you'd handle connection errors and retries.
    """
    try:
        producer = await KafkaProducerManager.get_producer()
        await producer.send_and_wait(topic, message)
    except Exception as e:
        # We don't want to crash the app if Kafka is down,
        print(f"Failed to publish to Kafka: {e}")
        raise e
