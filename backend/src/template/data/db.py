from typing import (
    TYPE_CHECKING,
    Callable,
    Generic,
    Literal,
    Sequence,
    TypeVar,
    Mapping,
)
from typing_extensions import TypedDict

from aiobotocore.session import get_session
from pydantic import BaseModel

from template.settings import AWS_REGION

if TYPE_CHECKING:
    from types_aiobotocore_dynamodb.type_defs import (
        AttributeDefinitionTypeDef,
        KeySchemaElementTypeDef,
        AttributeValueTypeDef,
    )

    DynamoItem = Mapping[str, AttributeValueTypeDef]


class DynamoDbSDict(TypedDict):
    S: str


class BaseAttributeValueDef(BaseModel):
    def __getitem__(self, item):
        return getattr(self, item)


T = TypeVar("T", bound=BaseModel)
U = TypeVar("U", bound=BaseAttributeValueDef)


class DynamoTable(Generic[T, U]):
    # DynamoDB allows a max of 100 items per batch
    BATCH_MAX = 100
    service: Literal["dynamodb"] = "dynamodb"
    region = AWS_REGION

    def __init__(
        self,
        table_name: str,
        primary_key: str,
        attribute_defs: Sequence["AttributeDefinitionTypeDef"],
        key_schema: Sequence["KeySchemaElementTypeDef"],
        serializer: Callable[[T], U],
        deserializer: Callable[["DynamoItem"], T],
    ):
        self.table_name = table_name
        self.primary_key = primary_key
        self.attribute_defs = attribute_defs
        self.key_schema = key_schema
        self.serializer = serializer
        self.deserializer = deserializer

    @property
    def client(self):
        session = get_session()
        client = session.create_client(self.service, region_name=self.region)
        return client

    async def get_or_create_table(self):
        async with self.client as client:
            try:
                return await client.describe_table(TableName=self.table_name)
            except client.exceptions.ResourceNotFoundException:
                return await client.create_table(
                    BillingMode="PAY_PER_REQUEST",
                    TableName=self.table_name,
                    AttributeDefinitions=self.attribute_defs,
                    KeySchema=self.key_schema,
                )

    async def save_item(self, item: T):
        async with self.client as client:
            await client.put_item(
                TableName=self.table_name,
                Item=self.serializer(item).model_dump(),
            )

    async def batch_save_items(self, items: list[T]):
        async with self.client as client:
            await client.batch_write_item(
                RequestItems={
                    self.table_name: [
                        {"PutRequest": {"Item": self.serializer(item).model_dump()}}
                        for item in items
                    ]
                }
            )

    async def get_all_primary_keys(self):
        async with self.client as client:
            response = await client.scan(
                TableName=self.table_name,
                ProjectionExpression=self.primary_key,
            )
            return [item[self.primary_key]["S"] for item in response["Items"]]

    async def get_all_primary_keys_batched(self):
        keys = await self.get_all_primary_keys()
        n_batches = len(keys) // DynamoTable.BATCH_MAX
        for b in range(n_batches + 1):
            batch = keys[b * DynamoTable.BATCH_MAX : (b + 1) * DynamoTable.BATCH_MAX]
            if batch:
                yield batch

    async def get_items(self, keys: list[str]):
        async with self.client as client:
            response = await client.batch_get_item(
                RequestItems={
                    self.table_name: {
                        "Keys": [{self.primary_key: {"S": key}} for key in keys]
                    }
                }
            )
            return {
                item[self.primary_key]["S"]: self.deserializer(item)
                for item in response["Responses"][self.table_name]
            }
