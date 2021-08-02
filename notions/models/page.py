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

    def get_value(self):
        return self.number


class SelectOption(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    color: Color

    def get_value(self):
        return self.color.value


class PageSelectProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["select"] = "select"
    select: SelectOption

    def get_value(self):
        return self.select.get_value()


class PageCreatedTimeProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["created_time"] = "created_time"
    created_time: datetime.datetime

    def get_value(self):
        return self.created_time


class PageLastEditedTimeProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: datetime.datetime

    def get_value(self):
        return self.last_edited_time


class PageURLProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["url"] = "url"
    url: str

    def get_value(self):
        return self.url


class PageTitleProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["title"] = "title"
    title: typing.List[RichText]

    def get_value(self):
        possible_titles = [title.get_value() for title in self.title]
        possible_titles = [title for title in possible_titles if title]
        if possible_titles:
            return possible_titles[0]
        return ""


class Relation(pydantic.BaseModel):
    id: uuid.UUID

    def get_value(self):
        return self.id


class PageRelationProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["relation"] = "relation"
    relation: typing.List[Relation]

    def get_value(self):
        return [relation.get_value() for relation in self.relation]


class PageRichTextProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["rich_text"] = "rich_text"
    rich_text: typing.List[RichText]

    def get_value(self):
        possible_values = [value.get_value() for value in self.rich_text]
        possible_values = [value for value in possible_values if value]
        if possible_values:
            return possible_values[0]
        return ""


class DateRange(pydantic.BaseModel):
    start: typing.Union[datetime.datetime, datetime.date]
    end: typing.Optional[typing.Union[datetime.datetime, datetime.date]]

    # TODO: decide if a dict or a dataclass or the daterange is a good return value
    def get_value(self):
        return {"start": self.start, "end": self.end}


class PageDateProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["date"] = "date"
    date: DateRange

    def get_value(self):
        return self.date


class PageFilesProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["files"] = "files"
    files: typing.List[typing.Dict[str, str]]

    def get_value(self):
        return self.files


class PagePeopleProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["people"] = "people"
    people: typing.List[User]

    def get_value(self):
        return [person.get_value() for person in self.people]


class PageCheckboxProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["checkbox"] = "checkbox"
    checkbox: bool

    def get_value(self):
        return self.checkbox


class PageEmailProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["email"] = "email"
    email: str

    def get_value(self):
        return self.email


class PagePhoneNumberProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["phone_number"] = "phone_number"
    phone_number: str

    def get_value(self):
        return self.phone_number


class MultiSelectOption(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    color: Color

    def get_value(self):
        return {"name": self.name, "color": self.color.value}


class PageMultiSelectProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["multi_select"] = "multi_select"
    multi_select: typing.List[MultiSelectOption]

    def get_value(self):
        return [option.get_value() for option in self.multi_select]


class StringFormula(pydantic.BaseModel):
    type: typing.Literal["string"] = "string"
    string: str

    def get_value(self):
        return self.string


class NumberFormula(pydantic.BaseModel):
    type: typing.Literal["number"] = "number"
    number: decimal.Decimal

    def get_value(self):
        return self.number


class BooleanFormula(pydantic.BaseModel):
    type: typing.Literal["boolean"] = "boolean"
    boolean: bool

    def get_value(self):
        return self.boolean


class DateFormula(pydantic.BaseModel):
    type: typing.Literal["date"] = "date"
    date: DateRange

    def get_value(self):
        return self.date.get_value()


class PageFormulaProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["formula"] = "formula"
    formula: typing.Union[StringFormula, NumberFormula, BooleanFormula, DateFormula]

    def get_value(self):
        return self.formula.get_value()


class NumberRollup(pydantic.BaseModel):
    type: typing.Literal["number"] = "number"
    number: decimal.Decimal

    def get_value(self):
        return self.number


class DateRollup(pydantic.BaseModel):
    type: typing.Literal["date"] = "date"
    date: typing.Optional[DateRange]

    def get_value(self):
        return self.date.get_value() if self.date else None


class ArrayRollup(pydantic.BaseModel):
    type: typing.Literal["array"] = "array"
    array: typing.List[dict]  # TODO: implement all the rollup array types

    def get_value(self):
        return self.array


class PageRollupProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["rollup"] = "rollup"
    rollup: typing.Union[NumberRollup, DateRollup, ArrayRollup]

    def get_value(self):
        return self.rollup.get_value()


class PageCreatedByProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["created_by"] = "created_by"
    created_by: User

    def get_value(self):
        return self.created_by.get_value()


class PageLastEditedByProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["last_edited_by"] = "last_edited_by"
    last_edited_by: User

    def get_value(self):
        return self.last_edited_by.get_value()


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
