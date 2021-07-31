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


class CreatedByProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["created_by"] = "created_by"
    created_by: dict = pydantic.Field(default_factory=dict)


class LastEditedTimeProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: dict = pydantic.Field(default_factory=dict)


class LastEditedByProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["last_edited_by"] = "last_edited_by"
    last_edited_by: dict = pydantic.Field(default_factory=dict)


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


class DateProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["date"] = "date"
    date: dict = pydantic.Field(default_factory=dict)


class FilesProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["files"] = "files"
    files: dict = pydantic.Field(default_factory=dict)


class PeopleProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["people"] = "people"
    people: dict = pydantic.Field(default_factory=dict)


class CheckboxProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["checkbox"] = "checkbox"
    checkbox: dict = pydantic.Field(default_factory=dict)


class EmailProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["email"] = "email"
    email: dict = pydantic.Field(default_factory=dict)


class PhoneNumberProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["phone_number"] = "phone_number"
    phone_number: dict = pydantic.Field(default_factory=dict)


class MultiSelectOption(pydantic.BaseModel):
    id: str
    name: str
    color: Color


class MultiSelectOptions(pydantic.BaseModel):
    options: typing.List[MultiSelectOption]


class MultiSelectProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["multi_select"] = "multi_select"
    multi_select: MultiSelectOptions


class Formula(pydantic.BaseModel):
    expression: str


class FormulaProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["formula"] = "formula"
    formula: Formula


class Rollup(pydantic.BaseModel):
    relation_property_name: str
    relation_property_id: str
    rollup_property_name: str
    rollup_property_id: str
    function: str  # TODO: change to an enum


class RollupProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["rollup"] = "rollup"
    rollup: Rollup


class Relation(pydantic.BaseModel):
    database_id: uuid.UUID
    synced_property_name: typing.Optional[str]
    synced_property_id: typing.Optional[str]


class RelationProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["relation"] = "relation"
    relation: Relation


Property = typing.Union[
    NumberProperty,
    SelectProperty,
    CreatedTimeProperty,
    URLProperty,
    TitleProperty,
    RichTextProperty,
    DateProperty,
    FilesProperty,
    PeopleProperty,
    CheckboxProperty,
    EmailProperty,
    PhoneNumberProperty,
    MultiSelectProperty,
    FormulaProperty,
    RollupProperty,
    CreatedByProperty,
    LastEditedTimeProperty,
    LastEditedByProperty,
    RelationProperty,
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
