"""Models for requests to Notion

Models for searches, creation and modification.
"""

import datetime
import decimal
import typing

import pydantic

from . import parent
from .color import Color
from .database import Properties as DatabaseProperties
from .rich_text import RichText


class CreateDatabaseRequest(pydantic.BaseModel):
    parent: parent.DatabaseParents
    title: typing.List[RichText]
    properties: DatabaseProperties


class PageNumberProperty(pydantic.BaseModel):
    type: typing.Literal["number"] = "number"
    number: decimal.Decimal


class SelectOption(pydantic.BaseModel):
    name: str
    color: Color


class PageSelectProperty(pydantic.BaseModel):
    type: typing.Literal["select"] = "select"
    select: SelectOption


class PageCreatedTimeProperty(pydantic.BaseModel):
    type: typing.Literal["created_time"] = "created_time"
    created_time: datetime.datetime


class PageURLProperty(pydantic.BaseModel):
    type: typing.Literal["url"] = "url"
    url: str


class PageTitleProperty(pydantic.BaseModel):
    type: typing.Literal["title"] = "title"
    title: typing.List[dict]


PageCreationProperties = typing.Union[
    PageNumberProperty,
    PageSelectProperty,
    PageCreatedTimeProperty,
    PageURLProperty,
    PageTitleProperty,
]


class CreatePageRequest(pydantic.BaseModel):
    parent: parent.PageParents
    properties: typing.Dict[str, PageCreationProperties]
    children: list  # TODO: define block types


class QueryDatabaseSort(pydantic.BaseModel):
    property: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None
    direction: typing.Literal["ascending", "descending"]


class QueryDatabaseRequest(pydantic.BaseModel):
    filter: typing.Optional[dict] = None  # TODO: define filter types
    sorts: typing.Optional[typing.List[QueryDatabaseSort]] = None
    start_cursor: typing.Optional[str] = None
    page_size: int = 100


class SearchFilter(pydantic.BaseModel):
    value: typing.Literal["page", "database"] = "page"
    property: typing.Literal["object"] = "object"


class SearchSort(pydantic.BaseModel):
    direction: typing.Literal["ascending", "descending"] = "ascending"
    timestamp: typing.Literal["last_edited_time"] = "last_edited_time"


# Small whinge: as it stands the search interface appears to be pretty broken (it never seems to match on query)
class SearchRequest(pydantic.BaseModel):
    query: typing.Optional[str] = None
    filter: typing.Optional[SearchFilter] = None
    sort: SearchSort = SearchSort()
    start_cursor: typing.Optional[str] = None
    page_size: int = 100
