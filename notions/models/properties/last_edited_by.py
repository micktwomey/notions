import typing

import pydantic

from ..user import User


class DatabaseLastEditedByProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["last_edited_by"] = "last_edited_by"
    last_edited_by: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.last_edited_by


class PageLastEditedByProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["last_edited_by"] = "last_edited_by"
    last_edited_by: User

    def get_value(self):
        return self.last_edited_by.get_value()
