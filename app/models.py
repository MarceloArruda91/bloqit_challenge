from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
import uuid


def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())


class RentStatus(Enum):
    CREATED = "CREATED"
    WAITING_DROPOFF = "WAITING_DROPOFF"
    WAITING_PICKUP = "WAITING_PICKUP"
    DELIVERED = "DELIVERED"


class RentSize(Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


@dataclass
class Rent:
    id: str = field(default_factory=generate_id)
    locker_id: Optional[str] = field(default=None, metadata={"data_key": "lockerId"})
    weight: float = 0.0
    size: RentSize = ""
    status: RentStatus = "CREATED"

    def update_status(self, new_status: RentStatus):
        self.status = new_status


class LockerStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass
class Locker:
    id: str = field(default_factory=generate_id)
    bloq_id: Optional[str] = field(default=None, metadata={"data_key": "bloqId"})
    status: LockerStatus = LockerStatus.OPEN
    is_occupied: bool = field(default=False, metadata={"data_key": "isOccupied"})

    def update_status(self, new_status: LockerStatus, occupied: bool):
        self.status = new_status
        self.is_occupied = occupied


@dataclass
class Bloq:
    id: str = field(default_factory=generate_id)
    title: str = ""
    address: str = ""
