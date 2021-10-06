import typing

import pydantic


class DatabaseCheckboxProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["checkbox"] = "checkbox"
    checkbox: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.checkbox


class PageCheckboxProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["checkbox"] = "checkbox"
    checkbox: bool

    def get_value(self):
        return self.checkbox
