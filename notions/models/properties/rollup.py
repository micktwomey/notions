import decimal
import enum
import typing

import pydantic

from ..date import DateRange


class RollupFunction(enum.Enum):
    count_all = "count_all"
    count_values = "count_values"
    count_unique_values = "count_unique_values"
    count_empty = "count_empty"
    count_not_empty = "count_not_empty"
    percent_empty = "percent_empty"
    percent_not_empty = "percent_not_empty"
    sum = "sum"
    average = "average"
    median = "median"
    min = "min"
    max = "max"
    range = "range"
    show_original = "show_original"
    # TODO: split date related rollups?
    date_range = "date_range"


class DatabaseRollup(pydantic.BaseModel):
    relation_property_name: str
    relation_property_id: str
    rollup_property_name: str
    rollup_property_id: str
    function: RollupFunction

    def get_value(self):
        return {
            "relation_property_name": self.relation_property_name,
            "relation_property_id": self.relation_property_id,
            "rollup_property_name": self.rollup_property_name,
            "rollup_property_id": self.rollup_property_id,
            "function": self.function.value,
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
    number: typing.Optional[decimal.Decimal]
    function: RollupFunction

    def get_value(self):
        return self.number


class PageDateRollup(pydantic.BaseModel):
    type: typing.Literal["date"] = "date"
    date: typing.Optional[DateRange]
    function: RollupFunction

    def get_value(self):
        return self.date.get_value() if self.date else None


class PageArrayRollup(pydantic.BaseModel):
    type: typing.Literal["array"] = "array"
    array: typing.List[dict]  # TODO: implement all the rollup array types
    function: RollupFunction

    def get_value(self):
        return self.array


class PageRollupProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["rollup"] = "rollup"
    rollup: typing.Union[PageNumberRollup, PageDateRollup, PageArrayRollup]

    def get_value(self):
        return self.rollup.get_value()
