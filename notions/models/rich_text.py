import typing

import pydantic

from .color import Color


class Annotations(pydantic.BaseModel):
    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    code: bool
    color: Color


class TextLink(pydantic.BaseModel):
    type: str = "url"
    url: str


class Text(pydantic.BaseModel):
    content: str
    link: typing.Optional[TextLink] = None


class RichTextText(pydantic.BaseModel):
    type: typing.Literal["text"] = "text"
    plain_text: str
    href: typing.Optional[str] = None
    annotations: Annotations = Annotations(
        bold=False,
        italic=False,
        strikethrough=False,
        underline=False,
        code=False,
        color=Color.default,
    )
    text: Text

    def get_value(self):
        return self.plain_text


RichText = RichTextText
