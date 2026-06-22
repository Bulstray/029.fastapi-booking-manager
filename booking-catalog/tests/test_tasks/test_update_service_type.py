import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import BookingCreate
from core.types import ServiceType
from storage.booking import crud as booking_crud
from tasks.update_service_type import update_service_type


@pytest.mark.anyio
async def test_update_service_type_worker_with_mock(
    session: AsyncSession,
) -> None:

    booking_create = BookingCreate(
        name="test",
        datetime=datetime.now(tz=UTC),
    )
    booking = await booking_crud.create_booking(
        session,
        booking_create,
    )

    with patch("asyncio.sleep", new_callable=AsyncMock):
        await update_service_type(booking.id, session)

        await asyncio.sleep(2)

        await session.refresh(booking)
        assert booking.service_type in (
            ServiceType.confirmed,
            ServiceType.failed,
        )
