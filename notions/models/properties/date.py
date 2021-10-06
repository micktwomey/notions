import datetime
import typing

import pydantic

from ..date import DateRange


class DatabaseDateProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["date"] = "date"
    date: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.date


class PageDateProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["date"] = "date"
    date: DateRange

    def get_value(self):
        return self.date
