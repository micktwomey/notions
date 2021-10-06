import decimal
import typing

import pydantic

from ..date import DateRange


class DatabaseFormula(pydantic.BaseModel):
    expression: str

    def get_value(self):
        return self.expression


class DatabaseFormulaProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["formula"] = "formula"
    formula: DatabaseFormula

    def get_value(self):
        return self.formula.get_value()


class PageStringFormula(pydantic.BaseModel):
    type: typing.Literal["string"] = "string"
    string: str

    def get_value(self):
        return self.string


class PageNumberFormula(pydantic.BaseModel):
    type: typing.Literal["number"] = "number"
    number: decimal.Decimal

    def get_value(self):
        return self.number


class PageBooleanFormula(pydantic.BaseModel):
    type: typing.Literal["boolean"] = "boolean"
    boolean: bool

    def get_value(self):
        return self.boolean


class PageDateFormula(pydantic.BaseModel):
    type: typing.Literal["date"] = "date"
    date: DateRange

    def get_value(self):
        return self.date.get_value()


class PageFormulaProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["formula"] = "formula"
    formula: typing.Union[
        PageStringFormula, PageNumberFormula, PageBooleanFormula, PageDateFormula
    ]

    def get_value(self):
        return self.formula.get_value()
