import json
from typing import List, Type, TypeVar, Optional, Generic
from dataclasses import fields, asdict
from app.utils import generate_id

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    A generic base repository class for managing data access and persistence.

    Attributes:
        data_file (str): The path to the JSON file storing the data.
        cls (Type[T]): The class type of the entity.
        data (List[T]): The in-memory list of entity instances.

    Methods:
        load_data(): Loads data from the JSON file into memory.
        map_data_keys(data: dict): Maps JSON keys to class attributes.
        get_all(): Returns all entity instances.
        get_by_id(entity_id: str): Returns an entity instance by its ID.
        add(entity: T): Adds a new entity instance.
        save(): Saves the current state of data to the JSON file.
    """

    def __init__(self, data_file: str, cls: Type[T]):
        """
        Initializes the BaseRepository with the given data file and class type.

        Parameters:
            data_file (str): The path to the JSON file.
            cls (Type[T]): The class type of the entity.
        """
        self.data_file = data_file
        self.cls = cls
        self.data = self.load_data()

    def load_data(self) -> List[T]:
        """
        Loads data from the JSON file into memory.

        Returns:
            List[T]: A list of entity instances.
        """
        with open(self.data_file, "r", encoding="utf-8") as f:
            return [self.cls(**self.map_data_keys(item)) for item in json.load(f)]

    def map_data_keys(self, data: dict) -> dict:
        """
        Maps JSON keys to class attributes using metadata.

        Parameters:
            data (dict): The dictionary to map keys.

        Returns:
            dict: The dictionary with mapped keys.
        """
        for field in fields(self.cls):
            data_key = field.metadata.get("data_key")
            if data_key and data_key in data:
                data[field.name] = data.pop(data_key)
        return data

    def get_all(self) -> List[T]:
        """
        Returns all entity instances.

        Returns:
            List[T]: A list of all entity instances.
        """
        return self.data

    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Returns an entity instance by its ID.

        Parameters:
            entity_id (str): The ID of the entity.

        Returns:
            Optional[T]: The entity instance, or None if not found.
        """
        return next((item for item in self.data if item.id == entity_id), None)

    def add(self, entity: T) -> T:
        """
        Adds a new entity instance.

        Parameters:
            entity (T): The entity instance to add.

        Returns:
            T: The added entity instance.
        """
        entity.id = generate_id()
        self.data.append(entity)
        self.save()
        return entity

    def save(self):
        """
        Saves the current state of data to the JSON file.
        """
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(
                [asdict(item) for item in self.data], f, ensure_ascii=False, indent=4
            )
