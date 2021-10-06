import datetime
import typing
import uuid

import pydantic

from .parent import DatabaseParents, PageParent
from .properties import CreateDatabaseProperties, DatabaseProperties
from .rich_text import RichText


class Database(pydantic.BaseModel):
    object: typing.Literal["database"] = "database"
    id: uuid.UUID
    created_time: datetime.datetime
    last_edited_time: datetime.datetime
    title: typing.List[RichText]
    parent: DatabaseParents
    properties: DatabaseProperties


class CreateDatabase(pydantic.BaseModel):
    parent: PageParent  # 2021-08-16 API only supports page parents
    title: typing.List[RichText]
    properties: CreateDatabaseProperties


# TODO: UpdateDatabase
