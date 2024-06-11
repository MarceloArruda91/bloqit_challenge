from app.base_repository import BaseRepository
from app.models import Bloq, Locker, Rent
from app.utils import select_unoccupied_locker
from typing import Optional


class BloqRepository(BaseRepository[Bloq]):
    """
    A repository class for managing Bloq entities.

    Inherits from BaseRepository[Bloq].
    """

    def __init__(self, data_file: str):
        """
        Initializes the BloqRepository with the given data file.

        Parameters:
            data_file (str): The path to the JSON file.
        """
        super().__init__(data_file, Bloq)


class LockerRepository(BaseRepository[Locker]):
    """
    A repository class for managing Locker entities.

    Inherits from BaseRepository[Locker].

    Methods:
        select_unoccupied(): Selects an unoccupied locker.
    """

    def __init__(self, data_file: str):
        """
        Initializes the LockerRepository with the given data file.

        Parameters:
            data_file (str): The path to the JSON file.
        """
        super().__init__(data_file, Locker)

    #This method is currently not being used
    def select_unoccupied(self) -> Optional[Locker]:
        """
        Selects an unoccupied locker.

        Returns:
            Optional[Locker]: An unoccupied locker, or None if none are available.
        """
        return select_unoccupied_locker(self.data)


class RentRepository(BaseRepository[Rent]):
    """
    A repository class for managing Rent entities.

    Inherits from BaseRepository[Rent].
    """

    def __init__(self, data_file: str):
        """
        Initializes the RentRepository with the given data file.

        Parameters:
            data_file (str): The path to the JSON file.
        """
        super().__init__(data_file, Rent)
