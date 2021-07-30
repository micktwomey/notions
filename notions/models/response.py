import typing

import pydantic

from .database import Database
from .page import Page


class PaginatedListResponse(pydantic.BaseModel):
    object: typing.Literal["list"] = "list"
    results: typing.List[typing.Union[Page, Database]]
    next_cursor: typing.Optional[str]
    has_more: bool
