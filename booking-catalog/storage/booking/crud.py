from sqlalchemy import update, select
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
) -> Booking:
    booking = Booking(**booking_in.model_dump())
    session.add(booking)
    await session.commit()
    return booking


async def update_service_type(
    session: AsyncSession,
    id_: int,
    service_type: ServiceType,
) -> None:
    stmt = update(Booking).where(Booking.id == id_).values(service_type=service_type)
    await session.execute(stmt)
    await session.commit()


async def delete_booking(session, booking: Booking) -> None:
    await session.delete(booking)
    await session.commit()


async def get_bookings(
    session: AsyncSession,
    service_type: str | None = None,
    page: int = 1,
    size: int = 10,
) -> list[Booking]:
    """Возвращает список броней с пагинацией и общее количество."""
    stmt = select(Booking)

    if service_type:
        stmt = stmt.where(Booking.service_type == service_type)

    offset = (page - 1) * size
    stmt = stmt.offset(offset).limit(size)

    result = await session.execute(stmt)
    bookings = result.scalars().all()

    return bookings
