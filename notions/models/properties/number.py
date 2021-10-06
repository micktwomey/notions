import decimal
import typing

import pydantic

from ..number import Number


class DatabaseNumberProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["number"] = "number"
    number: Number

    def get_value(self):
        return self.number.get_value()


class CreateDatabaseNumberProperty(pydantic.BaseModel):
    number: Number


class PageNumberProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["number"] = "number"
    number: decimal.Decimal

    def get_value(self):
        return self.number


class CreatePageNumberProperty(pydantic.BaseModel):
    type: typing.Literal["number"] = "number"
    number: decimal.Decimal
