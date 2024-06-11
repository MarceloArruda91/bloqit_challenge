from typing import List, Optional, Any
from app.base_repository import BaseRepository


class BaseService:
    """
    A generic base service class for handling business logic.

    Attributes:
        repository (BaseRepository): The repository instance for data access.
    """

    def __init__(self, repository: BaseRepository):
        """
        Initializes the BaseService with the given repository.

        Parameters:
            repository (BaseRepository): The repository instance.
        """
        self.repository = repository

    def get_all(self) -> List[Any]:
        """
        Returns all entity instances.

        Returns:
            List[Any]: A list of all entity instances.
        """
        return self.repository.get_all()

    def get_by_id(self, entity_id: str) -> Optional[Any]:
        """
        Returns an entity instance by its ID.

        Parameters:
            entity_id (str): The ID of the entity.

        Returns:
            Optional[Any]: The entity instance, or None if not found.
        """
        return self.repository.get_by_id(entity_id)

    def create(self, entity: Any) -> Any:
        """
        Creates a new entity instance.

        Parameters:
            entity (Any): The entity instance to create.

        Returns:
            Any: The created entity instance.
        """
        return self.repository.create(entity)
