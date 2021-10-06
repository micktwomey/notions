import typing

import pydantic

from ..user import User


class DatabaseCreatedByProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["created_by"] = "created_by"
    created_by: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.created_by


class PageCreatedByProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["created_by"] = "created_by"
    created_by: User

    def get_value(self):
        return self.created_by.get_value()
