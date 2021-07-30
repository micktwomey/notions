import datetime
import enum
import typing
import uuid

import pydantic

from .color import Color
from .number import Number
from .parent import DatabaseParents
from .rich_text import RichText


class NumberProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["number"] = "number"
    number: Number


class SelectOption(pydantic.BaseModel):
    id: str
    name: str
    color: Color


class Select(pydantic.BaseModel):
    options: typing.List[SelectOption]


class SelectProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["select"] = "select"
    select: Select


class CreatedTimeProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["created_time"] = "created_time"
    created_time: dict = pydantic.Field(default_factory=dict)


class URLProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["url"] = "url"
    url: dict = pydantic.Field(default_factory=dict)


class TitleProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["title"] = "title"
    title: dict = pydantic.Field(default_factory=dict)


class RichTextProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["rich_text"] = "rich_text"
    rich_text: dict = pydantic.Field(default_factory=dict)


Property = typing.Union[
    NumberProperty,
    SelectProperty,
    CreatedTimeProperty,
    URLProperty,
    TitleProperty,
    RichTextProperty,
]

Properties = typing.Dict[str, Property]


class Database(pydantic.BaseModel):
    object: typing.Literal["database"] = "database"
    id: uuid.UUID
    created_time: datetime.datetime
    last_edited_time: datetime.datetime
    title: typing.List[RichText]
    parent: DatabaseParents
    properties: Properties
