import random
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx2 import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Booking
from core.schemas import BookingCreate
from core.types import ServiceType
from storage.booking import crud as booking_crud

EXPECTED_BOOKINGS_COUNT = 5


async def create_test_booking(
    session: AsyncSession,
    booking: Booking,
) -> Booking:
    session.add(booking)
    await session.commit()
    await session.refresh(booking)
    return booking


@pytest.mark.anyio
async def test_list_bookings(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    list_service_type = list(ServiceType)
    list_bookings = [
        Booking(
            name=f"test{i}",
            service_type=random.choice(list_service_type),  # noqa: S311
            datetime=datetime.now(tz=UTC),
        )
        for i in range(20)
    ]

    session.add_all(list_bookings)

    await session.commit()

    response = await client.get(
        "/",
        params={"page": 1, "size": 5},
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == EXPECTED_BOOKINGS_COUNT


@pytest.mark.anyio
async def test_create_booking(
    client: AsyncClient,
    mock_taskiq: AsyncMock,
) -> None:
    response = await client.post(
        "/",
        json={
            "name": "test",
            "datetime": f"{datetime.now(tz=UTC)}",
        },
    )
    assert response.json() == {"message": "Booking is publisher"}
    assert response.status_code == status.HTTP_201_CREATED

    mock_taskiq.assert_called_once()


@pytest.mark.anyio
async def test_get_raise_by_id(client: AsyncClient) -> None:
    response = await client.get("/1000")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Booking not found"}


@pytest.mark.anyio
async def test_get_booking_by_id(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    booking_in = await booking_crud.create_booking(
        session,
        BookingCreate(name="test", datetime=datetime.now(tz=UTC)),
    )

    response = await client.get(f"/{booking_in.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"service_type": "pending"}


@pytest.mark.anyio
async def test_get_raised_delete_by_id(client: AsyncClient) -> None:
    response = await client.delete("/1000")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Booking not found"}


@pytest.mark.anyio
async def test_get_raised_if_service_type_not_pending(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    booking = Booking(
        name="test",
        service_type=ServiceType.confirmed,
        datetime=datetime.now(tz=UTC),
    )

    await create_test_booking(session, booking)

    response = await client.delete(f"/{booking.id}")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": (
            "Cannot delete booking: "
            "only bookings with 'pending' status can be deleted"
        ),
    }


@pytest.mark.anyio
async def test_delete_by_id(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    booking = Booking(
        name="test",
        service_type=ServiceType.pending,
        datetime=datetime.now(tz=UTC),
    )

    await create_test_booking(session, booking)

    response = await client.delete(f"/{booking.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
