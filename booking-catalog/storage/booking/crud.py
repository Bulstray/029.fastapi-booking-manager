from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Booking
from core.schemas import BookingCreate
from core.types import ServiceType


async def get_booking_by_id(
    session: AsyncSession,
    id_: int,
) -> Booking | None:
    return await session.get(Booking, id_)


async def create_booking(
    session: AsyncSession,
    booking_in: BookingCreate,
) -> None:
    booking = Booking(**booking_in.model_dump())
    session.add(booking)
    await session.commit()


async def update_service_type(
    session: AsyncSession,
    id_: int,
    service_type: ServiceType,
) -> None:
    stmt = update(Booking).where(Booking.id == id_).values(service_type=service_type)
    await session.execute(stmt)
    await session.commit()
