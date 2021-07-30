import datetime
import decimal
import typing
import uuid

import pydantic

from .color import Color
from .parent import PageParents
from .rich_text import RichText


class PageNumberProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["number"] = "number"
    number: decimal.Decimal


class PageSelect(pydantic.BaseModel):
    id: str
    name: str
    color: Color


class PageSelectProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["select"] = "select"
    select: PageSelect


class PageCreatedTimeProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["created_time"] = "created_time"
    created_time: datetime.datetime


class PageURLProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["url"] = "url"
    url: str


class PageTitleProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["title"] = "title"
    title: typing.List[dict]


class PageRelationProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["relation"] = "relation"
    relation: list  # TODO: better define relation type


class PageRichTextProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["rich_text"] = "rich_text"
    rich_text: typing.List[RichText]


# TODO: "multi_select", "date", "formula", "rollup", "people", "files", "checkbox", "email", "phone_number", "created_by", "last_edited_time", and "last_edited_by"
PageProperty = typing.Union[
    PageNumberProperty,
    PageSelectProperty,
    PageCreatedTimeProperty,
    PageURLProperty,
    PageTitleProperty,
    PageRelationProperty,
    PageRichTextProperty,
]

PageProperties = typing.Dict[str, PageProperty]


class Page(pydantic.BaseModel):
    object: typing.Literal["page"] = "page"
    id: uuid.UUID
    created_time: datetime.datetime
    last_edited_time: datetime.datetime
    archived: bool
    properties: PageProperties
    parent: PageParents
    url: str
