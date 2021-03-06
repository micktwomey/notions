import enum
import typing

import pydantic


class Direction(enum.Enum):
    ascending = "ascending"
    descending = "descending"


class QueryDatabaseSort(pydantic.BaseModel):
    property: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None
    direction: Direction


class QueryDatabase(pydantic.BaseModel):
    filter: typing.Optional[dict] = None  # TODO: define filter types
    sorts: typing.Optional[typing.List[QueryDatabaseSort]] = None
    start_cursor: typing.Optional[str] = None
    page_size: int = 100
