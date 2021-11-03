"""The different responses the API will give back

"""

import logging
import typing
from dataclasses import dataclass

import pydantic

from .database import Database
from .page import Page

LOG = logging.getLogger(__name__)


@dataclass
class NotionAPIResponse:
    """Notion API will always return a JSON object with an object property

    Note that this isn't using a pydantic model as we don't directly decode or encode this.
    """

    object: str
    obj: typing.Any

    @property
    def is_error(self):
        return self.object == "error"

    def get_error_response(self) -> "ErrorResponse":
        return ErrorResponse.parse_obj(self.obj)

    @property
    def is_list(self):
        return self.object == "list"

    def get_paginated_list_response(self) -> "PaginatedListResponse":
        return PaginatedListResponse.parse_obj(self.obj)

    @property
    def is_database(self):
        return self.object == "database"

    def get_database(self) -> Database:
        return Database.parse_obj(self.obj)

    @property
    def is_page(self):
        return self.object == "page"

    def get_page(self) -> Page:
        return Page.parse_obj(self.obj)


class ErrorResponse(pydantic.BaseModel):
    object: typing.Literal["error"] = "error"
    status: int
    code: str
    message: str


class PaginatedListResponse(pydantic.BaseModel):
    object: typing.Literal["list"] = "list"
    results: typing.List[dict]
    next_cursor: typing.Optional[str]
    has_more: bool

    def iter_results(self) -> typing.Iterable[typing.Union[Database, Page]]:
        """Iterate over the results, yielding Database or Page instances"""
        for result in self.results:
            LOG.debug(f"{result=}")
            result_type = result.get("object", None)
            if result_type == "database":
                yield Database.parse_obj(result)
            elif result_type == "page":
                yield Page.parse_obj(result)
            else:
                raise ValueError(f"Don't know how to parse {result=}")
