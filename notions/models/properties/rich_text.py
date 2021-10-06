import typing

import pydantic

from ..rich_text import RichText


class DatabaseRichTextProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["rich_text"] = "rich_text"
    rich_text: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.rich_text


class PageRichTextProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["rich_text"] = "rich_text"
    rich_text: typing.List[RichText]

    def get_value(self):
        possible_values = [value.get_value() for value in self.rich_text]
        possible_values = [value for value in possible_values if value]
        if possible_values:
            return possible_values[0]
        return ""
