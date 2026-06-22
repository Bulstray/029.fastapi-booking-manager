import random
from datetime import datetime

import pytest
from fastapi import status
from httpx2 import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import BookingCreate
from core.models import Booking
from storage.booking import crud as booking_crud
from core.types import ServiceType


async def create_test_booking(
    session: AsyncSession,
    booking: Booking,
) -> Booking:
    session.add(booking)
    await session.commit()
    await session.refresh(booking)
    return booking


@pytest.mark.anyio
async def test_list_bookings(client: AsyncClient, session: AsyncSession):
    list_service_type = list(ServiceType)
    list_bookings = [
        Booking(
            name=f"test{i}",
            service_type=random.choice(list_service_type),
            datetime=datetime.now(),
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
    assert len(response.json()) == 5


@pytest.mark.anyio
async def test_create_booking(client: AsyncClient, mock_taskiq):
    response = await client.post(
        "/",
        json={
            "name": "test",
            "datetime": f"{datetime.now()}",
        },
    )
    assert response.json() == {"message": "Booking is publisher"}
    assert response.status_code == status.HTTP_201_CREATED

    mock_taskiq.assert_called_once()


@pytest.mark.anyio
async def test_get_raise_by_id(client: AsyncClient):
    response = await client.get("/1000")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Booking not found"}


@pytest.mark.anyio
async def test_get_booking_by_id(client: AsyncClient, session: AsyncSession):
    booking_in = await booking_crud.create_booking(
        session,
        BookingCreate(name="test", datetime=datetime.now()),
    )

    response = await client.get(f"/{booking_in.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"service_type": "pending"}


@pytest.mark.anyio
async def test_get_raised_delete_by_id(client: AsyncClient):
    response = await client.delete("/1000")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Booking not found"}


@pytest.mark.anyio
async def test_get_raised_if_service_type_not_pending(
    client: AsyncClient,
    session: AsyncSession,
):
    booking = Booking(
        name="test",
        service_type=ServiceType.confirmed,
        datetime=datetime.now(),
    )

    await create_test_booking(session, booking)

    response = await client.delete(f"/{booking.id}")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": "Cannot delete booking: only bookings with 'pending' status can be deleted",
    }
    await session.delete(booking)
    await session.commit()


@pytest.mark.anyio
async def test_delete_by_id(
    client: AsyncClient,
    session: AsyncSession,
):
    booking = Booking(
        name="test",
        service_type=ServiceType.pending,
        datetime=datetime.now(),
    )

    await create_test_booking(session, booking)

    response = await client.delete(f"/{booking.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    await session.delete(booking)
    await session.commit()
