import typing
import uuid

import pydantic

from ..color import Color


class DatabaseMultiSelectOption(pydantic.BaseModel):
    id: str
    name: str
    color: Color

    def get_value(self):
        return self.color.value


class DatabaseMultiSelectOptions(pydantic.BaseModel):
    options: typing.List[DatabaseMultiSelectOption]

    def get_value(self):
        return [o.get_value() for o in self.options]


class DatabaseMultiSelectProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["multi_select"] = "multi_select"
    multi_select: DatabaseMultiSelectOptions

    def get_value(self):
        return self.multi_select.get_value()


class PageMultiSelectOption(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    color: Color

    def get_value(self):
        return {"name": self.name, "color": self.color.value}


class PageMultiSelectProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["multi_select"] = "multi_select"
    multi_select: typing.List[PageMultiSelectOption]

    def get_value(self):
        return [option.get_value() for option in self.multi_select]
