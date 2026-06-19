from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import Booking as BookingModel
from core.models import db_helper
from core.schemas import BookingRead
from storage.booking import crud as booking_crud

router = APIRouter(
    prefix=settings.api.v1.bookings,
)


@router.get(
    "/{id_}",
    response_model=BookingRead,
)
async def get_booking_by_id(
    id_: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.deps.session_getter),
    ],
) -> BookingModel:
    return await booking_crud.get_booking_by_id(session, id_)
