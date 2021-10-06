import datetime
import typing
import uuid

import pydantic

from .parent import PageParents
from .properties import CreatePageProperties, PageProperties


class Page(pydantic.BaseModel):
    object: typing.Literal["page"] = "page"
    id: uuid.UUID
    created_time: datetime.datetime
    last_edited_time: datetime.datetime
    archived: bool
    properties: PageProperties
    parent: PageParents
    url: str
    # TODO: icon
    # TODO: cover


class CreatePageDatabaseParent(pydantic.BaseModel):
    database_id: uuid.UUID


class CreatePagePageParent(pydantic.BaseModel):
    page_id: uuid.UUID


CreatePageParents = typing.Union[CreatePageDatabaseParent]


class CreatePage(pydantic.BaseModel):
    parent: CreatePageParents
    properties: CreatePageProperties
    children: list  # TODO: define block types
    # TODO: icon
    # TODO: cover


class UpdatePage(pydantic.BaseModel):
    properties: PageProperties
    archived: bool = False
    # TODO: icon
    # TODO: cover
