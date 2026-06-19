from collections.abc import AsyncGenerator

from fastapi import FastAPI

from core.models import db_helper
from core.taskiq_broker import broker


async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    if not broker.is_worker_process:
        await broker.startup()

    yield

    if not broker.is_worker_process:
        await broker.shutdown()

    await db_helper.dispose()
