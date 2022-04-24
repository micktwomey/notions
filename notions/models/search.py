import typing

import pydantic


class SearchFilter(pydantic.BaseModel):
    value: typing.Literal["page", "database"]
    property: typing.Literal["object"]


class SearchSort(pydantic.BaseModel):
    direction: typing.Literal["ascending", "descending"] = "ascending"
    timestamp: typing.Literal["last_edited_time"] = "last_edited_time"


class Search(pydantic.BaseModel):
    query: typing.Optional[str] = None
    filter: typing.Optional[SearchFilter] = None
    sort: SearchSort = SearchSort()
    start_cursor: typing.Optional[str] = None
    page_size: int = 100
