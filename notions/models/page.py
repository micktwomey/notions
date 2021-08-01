import datetime
import decimal
import typing
import uuid

import pydantic

from .color import Color
from .parent import PageParents
from .rich_text import RichText
from .user import User


class PageNumberProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["number"] = "number"
    number: decimal.Decimal


class SelectOption(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    color: Color


class PageSelectProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["select"] = "select"
    select: SelectOption


class PageCreatedTimeProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["created_time"] = "created_time"
    created_time: datetime.datetime


class PageLastEditedTimeProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: datetime.datetime


class PageURLProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["url"] = "url"
    url: str


class PageTitleProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["title"] = "title"
    title: typing.List[RichText]


class Relation(pydantic.BaseModel):
    id: uuid.UUID


class PageRelationProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["relation"] = "relation"
    relation: typing.List[Relation]


class PageRichTextProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["rich_text"] = "rich_text"
    rich_text: typing.List[RichText]


class DateRange(pydantic.BaseModel):
    start: typing.Union[datetime.datetime, datetime.date]
    end: typing.Optional[typing.Union[datetime.datetime, datetime.date]]


class PageDateProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["date"] = "date"
    date: DateRange


class PageFilesProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["files"] = "files"
    files: typing.List[typing.Dict[str, str]]


class PagePeopleProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["people"] = "people"
    people: typing.List[User]


class PageCheckboxProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["checkbox"] = "checkbox"
    checkbox: bool


class PageEmailProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["email"] = "email"
    email: str


class PagePhoneNumberProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["phone_number"] = "phone_number"
    phone_number: str


class MultiSelectOption(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    color: Color


class PageMultiSelectProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["multi_select"] = "multi_select"
    multi_select: typing.List[MultiSelectOption]


class StringFormula(pydantic.BaseModel):
    type: typing.Literal["string"] = "string"
    string: str


class NumberFormula(pydantic.BaseModel):
    type: typing.Literal["number"] = "number"
    number: decimal.Decimal


class BooleanFormula(pydantic.BaseModel):
    type: typing.Literal["boolean"] = "boolean"
    boolean: bool


class DateFormula(pydantic.BaseModel):
    type: typing.Literal["date"] = "date"
    date: DateRange


class PageFormulaProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["formula"] = "formula"
    formula: typing.Union[StringFormula, NumberFormula, BooleanFormula, DateFormula]


class NumberRollup(pydantic.BaseModel):
    type: typing.Literal["number"] = "number"
    number: decimal.Decimal


class DateRollup(pydantic.BaseModel):
    type: typing.Literal["date"] = "date"
    date: typing.Optional[DateRange]


class ArrayRollup(pydantic.BaseModel):
    type: typing.Literal["array"] = "array"
    array: typing.List[dict]  # TODO: implement all the rollup array types


class PageRollupProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["rollup"] = "rollup"
    rollup: typing.Union[NumberRollup, DateRollup, ArrayRollup]


class PageCreatedByProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["created_by"] = "created_by"
    created_by: User


class PageLastEditedByProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["last_edited_by"] = "last_edited_by"
    last_edited_by: User


PageProperty = typing.Union[
    PageNumberProperty,
    PageSelectProperty,
    PageCreatedTimeProperty,
    PageURLProperty,
    PageTitleProperty,
    PageRelationProperty,
    PageRichTextProperty,
    PageDateProperty,
    PageFilesProperty,
    PagePeopleProperty,
    PageCheckboxProperty,
    PageEmailProperty,
    PagePhoneNumberProperty,
    PageMultiSelectProperty,
    PageFormulaProperty,
    PageRollupProperty,
    PageCreatedByProperty,
    PageLastEditedTimeProperty,
    PageLastEditedByProperty,
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
