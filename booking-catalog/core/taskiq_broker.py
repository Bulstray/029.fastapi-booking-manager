import logging

from taskiq import TaskiqEvents, TaskiqState
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

from core.config import settings

log = logging.getLogger(__name__)

result_backend = RedisAsyncResultBackend(
    redis_url=settings.broker.url,
)

broker = RedisStreamBroker(
    url=settings.broker.url,
).with_result_backend(result_backend)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    log.info("Worker startup completed, got state %s", state)
