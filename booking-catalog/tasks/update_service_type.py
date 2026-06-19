import asyncio
import logging
import random
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from core.models import db_helper
from core.taskiq_broker import broker
from core.types import ServiceType
from storage.booking.crud import update_service_type

log = logging.getLogger(__name__)


@broker.task
async def update_service_type(
    service_id: int,
    session: Annotated[
        AsyncSession,
        TaskiqDepends(db_helper.session_getter),
    ],
) -> None:

    await asyncio.sleep(120)

    if random.random() < 0.15:
        await update_service_type(
            session,
            service_id,
            ServiceType.failed,
        )
    else:
        await update_service_type(
            session,
            service_id,
            ServiceType.confirmed,
        )
