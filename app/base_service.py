from typing import List, Optional, TypeVar, Generic
from app.base_repository import BaseRepository

T = TypeVar("T")


class BaseService(Generic[T]):
    """
    A generic base service class for handling business logic.

    Attributes:
        repository (BaseRepository[T]): The repository instance for data access.

    Methods:
        get_all(): Returns all entity instances.
        get_by_id(entity_id: str): Returns an entity instance by its ID.
        create(entity: T): Creates a new entity instance.
    """

    def __init__(self, repository: BaseRepository[T]):
        """
        Initializes the BaseService with the given repository.

        Parameters:
            repository (BaseRepository[T]): The repository instance.
        """
        self.repository = repository

    def get_all(self) -> List[T]:
        """
        Returns all entity instances.

        Returns:
            List[T]: A list of all entity instances.
        """
        return self.repository.get_all()

    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Returns an entity instance by its ID.

        Parameters:
            entity_id (str): The ID of the entity.

        Returns:
            Optional[T]: The entity instance, or None if not found.
        """
        return self.repository.get_by_id(entity_id)

    def create(self, entity: T) -> T:
        """
        Creates a new entity instance.

        Parameters:
            entity (T): The entity instance to create.

        Returns:
            T: The created entity instance.
        """
        return self.repository.add(entity)
