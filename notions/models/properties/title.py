import typing

import pydantic

from ..rich_text import RichText


class DatabaseTitleProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["title"] = "title"
    title: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.title


class CreateDatabaseTitleProperty(pydantic.BaseModel):
    title: dict = pydantic.Field(
        default_factory=dict
    )  # TODO: properly spec out create title property


class PageTitleProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["title"] = "title"
    title: typing.List[RichText]

    def get_value(self):
        possible_titles = [title.get_value() for title in self.title]
        possible_titles = [title for title in possible_titles if title]
        if possible_titles:
            return possible_titles[0]
        return ""


class CreatePageTitleProperty(pydantic.BaseModel):
    type: typing.Literal["title"] = "title"
    title: typing.List[typing.Union[dict, RichText]]
