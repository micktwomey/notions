import typing

import pydantic

from .database import Database
from .page import Page


class NotionAPIResponse(pydantic.BaseModel):
    object: str


class ErrorResponse(pydantic.BaseModel):
    object: typing.Literal["error"] = "error"
    status: int
    code: str
    message: str


class PaginatedListResponse(pydantic.BaseModel):
    object: typing.Literal["list"] = "list"
    results: typing.List[typing.Any]
    next_cursor: typing.Optional[str]
    has_more: bool

    def iter_results(self) -> typing.Iterable[typing.Union[Database, Page]]:
        """Iterate over the results, yielding Database or Page instances"""
        for result in self.results:
            result_type = result.get("object", None)
            if result_type == "database":
                yield Database.parse_obj(result)
            elif result_type == "page":
                yield Page.parse_raw(result)
            else:
                raise ValueError(f"Don't know how to parse {result=}")
