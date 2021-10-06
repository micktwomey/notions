import decimal
import typing

import pydantic

from ..date import DateRange


class DatabaseRollup(pydantic.BaseModel):
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


class DatabaseRollupProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["rollup"] = "rollup"
    rollup: DatabaseRollup

    def get_value(self):
        return self.rollup.get_value()


class PageNumberRollup(pydantic.BaseModel):
    type: typing.Literal["number"] = "number"
    number: decimal.Decimal

    def get_value(self):
        return self.number


class PageDateRollup(pydantic.BaseModel):
    type: typing.Literal["date"] = "date"
    date: typing.Optional[DateRange]

    def get_value(self):
        return self.date.get_value() if self.date else None


class PageArrayRollup(pydantic.BaseModel):
    type: typing.Literal["array"] = "array"
    array: typing.List[dict]  # TODO: implement all the rollup array types

    def get_value(self):
        return self.array


class PageRollupProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["rollup"] = "rollup"
    rollup: typing.Union[PageNumberRollup, PageDateRollup, PageArrayRollup]

    def get_value(self):
        return self.rollup.get_value()
