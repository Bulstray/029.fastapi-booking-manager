from datetime import datetime

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.types import ServiceType

from .base import Base
from .mixin import IntIdPkMixin


class Booking(IntIdPkMixin, Base):
    __tablename__ = "bookings"

    name: Mapped[str]
    datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
    )
    service_type: Mapped[ServiceType] = mapped_column(
        Enum(ServiceType),
        default=ServiceType.pending,
        server_default=ServiceType.pending,
    )
