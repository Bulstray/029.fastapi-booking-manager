from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Booking


async def get_booking_by_id(
    session: AsyncSession,
    id_: int,
) -> Booking | None:
    return await session.get(Booking, id_)
