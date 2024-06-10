from typing import Optional
from app.models import Bloq, Locker, Rent, RentStatus, LockerStatus
from app.repositories import BloqRepository, LockerRepository, RentRepository
from app.base_service import BaseService


class BloqService(BaseService[Bloq]):
    """
    A service class for handling business logic related to Bloq entities.

    Inherits from BaseService[Bloq].
    """

    def __init__(self, repository: BloqRepository):
        """
        Initializes the BloqService with the given repository.

        Parameters:
            repository (BloqRepository): The repository instance.
        """
        super().__init__(repository)


class LockerService(BaseService[Locker]):
    """
    A service class for handling business logic related to Locker entities.

    Inherits from BaseService[Locker].

    Methods:
        select_unoccupied_locker(): Selects an unoccupied locker.
        update_locker_status(locker_id: str, status: LockerStatus, occupied: bool): Updates the status of a locker.
    """

    def __init__(self, repository: LockerRepository):
        """
        Initializes the LockerService with the given repository.

        Parameters:
            repository (LockerRepository): The repository instance.
        """
        super().__init__(repository)
        self.repository: LockerRepository = repository

    def select_unoccupied_locker(self) -> Optional[Locker]:
        """
        Selects an unoccupied locker.

        Returns:
            Optional[Locker]: An unoccupied locker, or None if none are available.
        """
        return self.repository.select_unoccupied()

    def update_locker_status(
        self, locker_id: str, status: LockerStatus, occupied: bool
    ) -> Optional[Locker]:
        """
        Updates the status of a locker.

        Parameters:
            locker_id (str): The ID of the locker to update.
            status (LockerStatus): The new status of the locker.
            occupied (bool): Whether the locker is occupied.

        Returns:
            Optional[Locker]: The updated locker, or None if not found.
        """
        locker = self.get_by_id(locker_id)
        if locker:
            locker.update_status(status, occupied)
            self.repository.save()
        return locker


class RentService(BaseService[Rent]):
    """
    A service class for handling business logic related to Rent entities.

    Inherits from BaseService[Rent].

    Attributes:
        locker_service (LockerService): The locker service instance for coordinating locker operations.

    Methods:
        create_rent(rent: Rent, locker_id: str): Creates a new rent and assigns the specified locker.
        update_rent_status(rent_id: str, status: RentStatus): Updates the status of a rent.
    """

    def __init__(self, repository: RentRepository, locker_service: LockerService):
        """
        Initializes the RentService with the given repository and locker service.

        Parameters:
            repository (RentRepository): The repository instance.
            locker_service (LockerService): The locker service instance.
        """
        super().__init__(repository)
        self.locker_service = locker_service

    def create_rent(self, rent: Rent, locker_id: str) -> Optional[Rent]:
        """
        Creates a new rent and assigns the specified locker.

        Parameters:
            rent (Rent): The rent instance to create.
            locker_id (str): The ID of the locker to assign.

        Returns:
            Optional[Rent]: The created rent instance, or None if the locker is not found or is occupied.
        """
        locker = self.locker_service.get_by_id(locker_id)
        if locker and not locker.is_occupied:
            rent.locker_id = locker.id
            rent.status = "CREATED"
            locker.update_status(LockerStatus.CLOSED, True)
            self.locker_service.repository.save()
            return self.repository.add(rent)
        return None

    def update_rent_status(self, rent_id: str, status: RentStatus) -> Optional[Rent]:
        """
        Updates the status of a rent.

        Parameters:
            rent_id (str): The ID of the rent to update.
            status (RentStatus): The new status of the rent.

        Returns:
            Optional[Rent]: The updated rent, or None if not found.
        """
        rent = self.get_by_id(rent_id)
        if rent:
            rent.update_status(status)
            self.repository.save()
        return rent
