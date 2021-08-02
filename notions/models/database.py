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

    def get_value(self):
        return self.number.get_value()


class SelectOption(pydantic.BaseModel):
    id: str
    name: str
    color: Color

    def get_value(self):
        return self.color.value


class Select(pydantic.BaseModel):
    options: typing.List[SelectOption]

    def get_value(self):
        return [o.get_value() for o in self.options]


class SelectProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["select"] = "select"
    select: Select

    def get_value(self):
        return self.select.get_value()


class CreatedTimeProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["created_time"] = "created_time"
    created_time: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.created_time


class CreatedByProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["created_by"] = "created_by"
    created_by: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.created_by


class LastEditedTimeProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.last_edited_time


class LastEditedByProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["last_edited_by"] = "last_edited_by"
    last_edited_by: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.last_edited_by


class URLProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["url"] = "url"
    url: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.url


class TitleProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["title"] = "title"
    title: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.title


class RichTextProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["rich_text"] = "rich_text"
    rich_text: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.rich_text


class DateProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["date"] = "date"
    date: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.date


class FilesProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["files"] = "files"
    files: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.files


class PeopleProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["people"] = "people"
    people: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.people


class CheckboxProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["checkbox"] = "checkbox"
    checkbox: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.checkbox


class EmailProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["email"] = "email"
    email: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.email


class PhoneNumberProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["phone_number"] = "phone_number"
    phone_number: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.phone_number


class MultiSelectOption(pydantic.BaseModel):
    id: str
    name: str
    color: Color

    def get_value(self):
        return self.color.value


class MultiSelectOptions(pydantic.BaseModel):
    options: typing.List[MultiSelectOption]

    def get_value(self):
        return [o.get_value() for o in self.options]


class MultiSelectProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["multi_select"] = "multi_select"
    multi_select: MultiSelectOptions

    def get_value(self):
        return self.multi_select.get_value()


class Formula(pydantic.BaseModel):
    expression: str

    def get_value(self):
        return self.expression


class FormulaProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["formula"] = "formula"
    formula: Formula

    def get_value(self):
        return self.formula.get_value()


class Rollup(pydantic.BaseModel):
    relation_property_name: str
    relation_property_id: str
    rollup_property_name: str
    rollup_property_id: str
    function: str  # TODO: change to an enum

    def get_value(self):
        return {
            "relation_property_name": self.relation_property_name,
            "relation_property_id": self.relation_property_id,
            "rollup_property_name": self.rollup_property_name,
            "rollup_property_id": self.rollup_property_id,
            "function": self.function,
        }


class RollupProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["rollup"] = "rollup"
    rollup: Rollup

    def get_value(self):
        return self.rollup.get_value()


class Relation(pydantic.BaseModel):
    database_id: uuid.UUID
    synced_property_name: typing.Optional[str]
    synced_property_id: typing.Optional[str]

    def get_value(self):
        return {
            "database_id": self.database_id,
            "synced_property_name": self.synced_property_name,
            "synced_property_id": self.synced_property_id,
        }


class RelationProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["relation"] = "relation"
    relation: Relation

    def get_value(self):
        return self.relation.get_value()


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
