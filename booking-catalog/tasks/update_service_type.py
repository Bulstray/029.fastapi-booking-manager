import asyncio
import logging
import random
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from core import broker
from core.models import db_helper
from core.types import ServiceType
from storage.booking import crud as booking_crud

log = logging.getLogger(__name__)


@broker.task
async def update_service_type(
    service_id: int,
    session: Annotated[
        AsyncSession,
        TaskiqDepends(db_helper.session_getter),
    ],
) -> None:

    await asyncio.sleep(60)

    if random.random() < 0.15:
        new_status = ServiceType.failed
        await booking_crud.update_service_type(
            session,
            service_id,
            ServiceType.failed,
        )
        log.info("Booking %s confirmed", service_id)
    else:
        new_status = ServiceType.confirmed
        await booking_crud.update_service_type(
            session,
            service_id,
            ServiceType.confirmed,
        )
        log.info("Booking %s failed", service_id)

    log.info(
        f"📧 [MOCK] Notification sent for booking %s: status=%s", service_id, new_status
    )
