import typing
import uuid

import pydantic

from ..color import Color


class DatabaseSelectOption(pydantic.BaseModel):
    id: str
    name: str
    color: Color

    def get_value(self):
        return self.color.value


class DatabaseSelect(pydantic.BaseModel):
    options: typing.List[DatabaseSelectOption]

    def get_value(self):
        return [o.get_value() for o in self.options]


class DatabaseSelectProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["select"] = "select"
    select: DatabaseSelect

    def get_value(self):
        return self.select.get_value()


# TODO: CreateDatabaseSelectProperty


class PageSelectOption(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    color: Color

    def get_value(self):
        return self.color.value


class PageSelectProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["select"] = "select"
    select: PageSelectOption

    def get_value(self):
        return self.select.get_value()


class CreatePageSelectOption(pydantic.BaseModel):
    name: str
    color: Color


class CreatePageSelectProperty(pydantic.BaseModel):
    type: typing.Literal["select"] = "select"
    select: CreatePageSelectOption
