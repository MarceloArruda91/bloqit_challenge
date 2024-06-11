import json
from typing import List, Type, Optional, Dict, Any
from dataclasses import fields, asdict
from app.utils import generate_id
from enum import Enum


class BaseRepository:
    """
    A generic base repository class for managing data access and persistence.

    Attributes:
        __data_file (str): The path to the JSON file storing the data.
        __cls (Type[Any]): The class type of the entity.
        __data (List[Any]): The in-memory list of entity instances.

    Methods:
        load_data(): Loads data from the JSON file into memory.
        map_data_keys(data: dict) -> dict: Maps JSON keys to class attributes.
        get_all() -> List[Any]: Returns all entity instances.
        get_by_id(entity_id: str) -> Optional[Any]: Returns an entity instance by its ID.
        create(entity: Any) -> Any: Adds a new entity instance.
        save_data(): Saves the current state of data to the JSON file.
        serialize_entity(entity: Any) -> Dict[str, Any]: Serializes an entity to a dictionary.
    """

    def __init__(self, data_file: str, cls: Any):
        """
        Initializes the BaseRepository with the given data file and class type.

        Parameters:
            data_file (str): The path to the JSON file.
            cls (Type[Any]): The class type of the entity.
        """
        self.__data_file = data_file
        self.__cls = cls
        self.__data = self.load_data()

    def load_data(self) -> List[Any]:
        """
        Loads data from the JSON file into memory.

        Returns:
            List[Any]: A list of entity instances.
        """
        with open(self.__data_file, "r", encoding="utf-8") as f:
            return [self.__cls(**self.map_data_keys(item)) for item in json.load(f)]

    def map_data_keys(self, data: dict) -> Dict[str, Any]:
        """
        Maps JSON keys to class attributes using metadata.

        Parameters:
            data (dict): The dictionary to map keys.

        Returns:
            dict: The dictionary with mapped keys.
        """
        for field in fields(self.__cls):
            data_key = field.metadata.get("data_key")
            if data_key in data:
                data[field.name] = data.pop(data_key)
        return data

    def get_all(self) -> List[Any]:
        """
        Returns all entity instances.

        Returns:
            List[Any]: A list of all entity instances.
        """
        return self.__data

    def get_by_id(self, entity_id: str) -> Optional[Any]:
        """
        Returns an entity instance by its ID.

        Parameters:
            entity_id (str): The ID of the entity.

        Returns:
            Optional[Any]: The entity instance, or None if not found.
        """
        return next((item for item in self.__data if item.id == entity_id), None)

    def create(self, entity: Any) -> Any:
        """
        Adds a new entity instance.

        Parameters:
            entity (Any): The entity instance to add.

        Returns:
            Any: The added entity instance.
        """
        entity.id = generate_id()
        self.__data.append(entity)
        self.save_data()
        return entity

    def save_data(self):
        """
        Saves the current state of data to the JSON file.
        """
        with open(self.__data_file, "w", encoding="utf-8") as f:
            json.dump(
                [self.serialize_entity(item) for item in self.__data],
                f,
                ensure_ascii=False,
                indent=4,
            )

    def serialize_entity(self, entity: Any) -> Dict[str, Any]:
        """
        Serializes an entity to a dictionary, converting Enums to their values.

        Parameters:
            entity (Any): The entity instance to serialize.

        Returns:
            Dict[str, Any]: The serialized entity as a dictionary.
        """
        entity_dict = asdict(entity)
        for field in fields(self.__cls):
            value = entity_dict.get(field.name)
            if isinstance(value, Enum):
                entity_dict[field.name] = value.value
        return entity_dict
