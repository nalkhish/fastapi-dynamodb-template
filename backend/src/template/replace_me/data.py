import json
from typing import TYPE_CHECKING

from pydantic import BaseModel

from template.data.db import (
    DynamoTable,
    DynamoDbSDict,
    BaseAttributeValueDef,
)
from template.data.manage import BaseManager

if TYPE_CHECKING:
    from template.data.db import DynamoItem


class ReplaceMe(BaseModel):
    id: str
    other_field: dict[str, str]


class ReplaceMeAttributeValueDef(BaseAttributeValueDef):
    id: DynamoDbSDict
    other_field: DynamoDbSDict


class ReplaceMeManager(BaseManager[ReplaceMe, ReplaceMeAttributeValueDef]):
    @staticmethod
    def serializer(item: ReplaceMe) -> ReplaceMeAttributeValueDef:
        return ReplaceMeAttributeValueDef(
            id={
                "S": item.id,
            },
            other_field={"S": json.dumps(item.other_field)},
        )

    @staticmethod
    def deserializer(unvalidated: "DynamoItem") -> ReplaceMe:
        item = ReplaceMeAttributeValueDef(**unvalidated)  # type: ignore
        return ReplaceMe(
            id=item["id"]["S"], other_field=json.loads(item["other_field"]["S"])
        )

    db = DynamoTable(
        table_name="replace_mes",
        primary_key="id",
        attribute_defs=[
            {"AttributeName": "id", "AttributeType": "S"},
        ],
        key_schema=[
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        serializer=serializer,
        deserializer=deserializer,
    )

    @classmethod
    def get_db(cls):
        return cls.db
