from enum import StrEnum


class ServiceType(StrEnum):
    pending = "pending"
    confirmed = "confirmed"
    failed = "failed"
