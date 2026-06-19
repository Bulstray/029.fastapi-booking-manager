from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Booking
from core.schemas import BookingCreate


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
