import uuid


def generate_id():
    return str(uuid.uuid4())


def select_unoccupied_locker(lockers):
    for locker in lockers:
        if not locker.is_occupied:
            return locker
    return None
