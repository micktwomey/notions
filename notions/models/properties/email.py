import typing

import pydantic


class DatabaseEmailProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["email"] = "email"
    email: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.email


class PageEmailProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["email"] = "email"
    email: str

    def get_value(self):
        return self.email
