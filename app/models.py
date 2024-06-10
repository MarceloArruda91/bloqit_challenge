from enum import Enum
from dataclasses import dataclass, field


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
    id: str
    locker_id: str = field(metadata={"data_key": "lockerId"})
    weight: float
    size: RentSize
    status: RentStatus

    def update_status(self, new_status: RentStatus):
        self.status = new_status


class LockerStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass
class Locker:
    id: str
    bloq_id: str = field(metadata={"data_key": "bloqId"})
    status: LockerStatus
    is_occupied: bool = field(metadata={"data_key": "isOccupied"})

    def update_status(self, new_status: LockerStatus, occupied: bool):
        self.status = new_status
        self.is_occupied = occupied


@dataclass
class Bloq:
    id: str
    title: str
    address: str
