from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import Booking as BookingModel
from core.models import db_helper
from core.schemas import BookingCreate, BookingRead
from storage.booking import crud as booking_crud
from core.types import ServiceType

from tasks import update_service_type

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
        Depends(db_helper.session_getter),
    ],
) -> BookingModel:
    if booking := await booking_crud.get_booking_by_id(session, id_):
        return booking

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Booking not found",
    )


@router.post("/")
async def create_booking(
    booking_in: BookingCreate,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> dict[str, str]:
    booking = await booking_crud.create_booking(session, booking_in)
    await update_service_type.kiq(booking.id)
    return {
        "message": "Booking is publisher",
    }


@router.delete(
    "/{id_}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_booking(
    id_: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> None:
    booking = await booking_crud.get_booking_by_id(session, id_)

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    if booking.service_type != ServiceType.pending:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete booking: only bookings with 'pending' status can be deleted",
        )

    await booking_crud.delete_booking(session, booking)
