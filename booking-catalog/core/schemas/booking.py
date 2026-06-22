from datetime import datetime

from pydantic import BaseModel

from core.types import ServiceType


class BookingBase(BaseModel):
    name: str
    datetime: datetime


class BookingRead(BaseModel):
    service_type: ServiceType


class BookingReadList(BookingRead):
    """Модель списка всех записей"""


class BookingCreate(BookingBase):
    """Модель для создания брони"""
