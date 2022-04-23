import datetime
import typing
import uuid

import pydantic

from .emoji import Emoji
from .file import PageCover
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
    icon: typing.Optional[Emoji]
    cover: typing.Optional[PageCover]


class CreatePageDatabaseParent(pydantic.BaseModel):
    database_id: uuid.UUID


class CreatePagePageParent(pydantic.BaseModel):
    page_id: uuid.UUID


CreatePageParents = CreatePageDatabaseParent


class CreatePage(pydantic.BaseModel):
    parent: CreatePageParents
    properties: CreatePageProperties
    children: list  # TODO: define block types
    icon: typing.Optional[Emoji] = None
    cover: typing.Optional[PageCover] = None


class UpdatePage(pydantic.BaseModel):
    properties: PageProperties
    archived: bool = False
    icon: typing.Optional[Emoji] = None
    cover: typing.Optional[PageCover] = None
