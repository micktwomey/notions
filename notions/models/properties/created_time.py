import datetime
import typing

import pydantic


class DatabaseCreatedTimeProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["created_time"] = "created_time"
    created_time: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.created_time


class PageCreatedTimeProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["created_time"] = "created_time"
    created_time: datetime.datetime

    def get_value(self):
        return self.created_time


class CreatePageCreatedTimeProperty(pydantic.BaseModel):
    type: typing.Literal["created_time"] = "created_time"
    created_time: datetime.datetime
