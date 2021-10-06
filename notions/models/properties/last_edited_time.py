import datetime
import typing

import pydantic


class DatabaseLastEditedTimeProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.last_edited_time


class PageLastEditedTimeProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: datetime.datetime

    def get_value(self):
        return self.last_edited_time
