import typing

import pydantic


class PaginatedListResponse(pydantic.BaseModel):
    object: typing.Literal["list"] = "list"
    results: list
    next_cursor: typing.Optional[str]
    has_more: bool
