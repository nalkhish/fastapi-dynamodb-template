from typing import Generic, TypeVar, TYPE_CHECKING
from abc import ABC, abstractmethod

from pydantic import BaseModel

from template.data.db import DynamoTable, BaseAttributeValueDef

if TYPE_CHECKING:
    from template.data.db import DynamoItem

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U", bound=BaseAttributeValueDef)


class BaseManager(Generic[T, U], ABC):
    """Manage a corresponding pydantic.BaseModel subclass

    This does everything for a model except representation/validation:
    - Facade to the db
    - Create new model instances
    """

    @staticmethod
    @abstractmethod
    def serializer(item: T) -> U:
        ...

    @staticmethod
    @abstractmethod
    def deserializer(item: "DynamoItem") -> T:
        ...

    @classmethod
    @abstractmethod
    def get_db(cls) -> DynamoTable[T, U]:
        ...

    @classmethod
    def get_or_create_table(cls):
        return cls.get_db().get_or_create_table()

    @classmethod
    def save(cls, item: T):
        return cls.get_db().save_item(item)

    @classmethod
    def save_batch(cls, items: list[T]):
        return cls.get_db().batch_save_items(items)

    @classmethod
    def get_all_primary_keys(cls):
        return cls.get_db().get_all_primary_keys()

    @classmethod
    def get_all_primary_keys_batched(cls):
        return cls.get_db().get_all_primary_keys_batched()

    @classmethod
    def get_items(cls, keys: list[str]):
        return cls.get_db().get_items(keys)
