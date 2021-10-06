import typing

import pydantic


class DatabaseURLProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["url"] = "url"
    url: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.url


class PageURLProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["url"] = "url"
    url: str

    def get_value(self):
        return self.url


class CreatePageURLProperty(pydantic.BaseModel):
    type: typing.Literal["url"] = "url"
    url: str
