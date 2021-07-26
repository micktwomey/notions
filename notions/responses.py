import datetime
import enum
import uuid
import typing

import pydantic


class Color(enum.Enum):
    default = "default"
    gray = "gray"
    brown = "brown"
    orange = "orange"
    yellow = "yellow"
    green = "green"
    blue = "blue"
    purple = "purple"
    pink = "pink"
    red = "red"
    gray_background = "gray_background"
    brown_background = "brown_background"
    orange_background = "orange_background"
    yellow_background = "yellow_background"
    green_background = "green_background"
    blue_background = "blue_background"
    purple_background = "purple_background"
    pink_background = "pink_background"
    red_background = "red_background"


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
    link: typing.Optional[TextLink]


class RichTextText(pydantic.BaseModel):
    type: typing.Literal["text"]
    plain_text: str
    href: typing.Optional[str]
    annotations: Annotations
    text: Text


RichText = typing.Union[RichTextText]


class PageParent(pydantic.BaseModel):
    type: typing.Literal["page_id"]
    page_id: uuid.UUID


class WorkspaceParent(pydantic.BaseModel):
    type: typing.Literal["workspace"] = "workspace"
    workspace: typing.Literal[True] = True


Parent = typing.Union[PageParent, WorkspaceParent]


class NumberFormat(enum.Enum):
    number = "number"
    number_with_commas = "number_with_commas"
    percent = "percent"
    dollar = "dollar"
    canadian_dollar = "canadian_dollar"
    euro = "euro"
    pound = "pound"
    yen = "yen"
    ruble = "ruble"
    rupee = "rupee"
    won = "won"
    yuan = "yuan"
    real = "real"
    lira = "lira"
    rupiah = "rupiah"
    franc = "franc"
    hong_kong_dollar = "hong_kong_dollar"
    new_zealand_dollar = "new_zealand_dollar"
    krona = "krona"
    norwegian_krone = "norwegian_krone"
    mexican_peso = "mexican_peso"
    rand = "rand"
    new_taiwan_dollar = "new_taiwan_dollar"
    danish_krone = "danish_krone"
    zloty = "zloty"
    baht = "baht"
    forint = "forint"
    koruna = "koruna"
    shekel = "shekel"
    chilean_peso = "chilean_peso"
    philippine_peso = "philippine_peso"
    dirham = "dirham"
    colombian_peso = "colombian_peso"
    riyal = "riyal"
    ringgit = "ringgit"
    leu = "leu"


class Number(pydantic.BaseModel):
    format: NumberFormat


class NumberProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["number"] = "number"
    number: Number


class SelectOption(pydantic.BaseModel):
    id: str
    name: str
    color: Color


class Select(pydantic.BaseModel):
    options: list[SelectOption]


class SelectProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["select"] = "select"
    select: Select


class CreatedTimeProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["created_time"] = "created_time"
    created_time: dict = pydantic.Field(default_factory=dict)


class URLProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["url"] = "url"
    url: dict = pydantic.Field(default_factory=dict)


class TitleProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["title"] = "title"
    title: dict = pydantic.Field(default_factory=dict)


Property = typing.Union[
    NumberProperty, SelectProperty, CreatedTimeProperty, URLProperty, TitleProperty
]

Properties = dict[str, Property]


class Database(pydantic.BaseModel):
    object: typing.Literal["database"]
    id: uuid.UUID
    created_time: datetime.datetime
    last_edited_time: datetime.datetime
    title: list[RichText]
    parent: Parent
    properties: Properties


class PaginatedListResponse(pydantic.BaseModel):
    object: typing.Literal["list"] = "list"
    results: list
    next_cursor: typing.Optional[str]
    has_more: bool
