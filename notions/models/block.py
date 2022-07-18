from __future__ import annotations

"""Represents blocks

https://developers.notion.com/reference/block
"""
import abc
import datetime
import enum
import typing
import uuid

import pydantic

import notions.models.file
from notions.models.color import Color
from notions.models.emoji import Emoji
from notions.models.rich_text import RichText


class BaseBlock(pydantic.BaseModel, abc.ABC):
    object: typing.Literal["block"] = "block"
    id: uuid.UUID
    created_time: datetime.datetime
    created_by: dict  # TODO: partial user
    last_edited_time: datetime.datetime
    last_edited_by: dict  # TODO: partial user
    archived: bool
    has_children: bool


class ParagraphBlock(BaseBlock):
    type: typing.Literal["paragraph"] = "paragraph"
    rich_text: list[RichText]
    color: Color
    children: list[Block]


class Heading1(pydantic.BaseModel):
    rich_text: list[RichText]
    color: Color


class Heading1Block(BaseBlock):
    type: typing.Literal["heading_1"] = "heading_1"
    heading_1: Heading1


class Heading2(pydantic.BaseModel):
    rich_text: list[RichText]
    color: Color


class Heading2Block(BaseBlock):
    type: typing.Literal["heading_2"] = "heading_2"
    heading_2: Heading2


class Heading3(pydantic.BaseModel):
    rich_text: list[RichText]
    color: Color


class Heading3Block(BaseBlock):
    type: typing.Literal["heading_3"] = "heading_3"
    heading_3: Heading3


class Callout(pydantic.BaseModel):
    rich_text: list[RichText]
    icon: typing.Union[notions.models.file.File, Emoji]
    color: Color
    children: list[Block]


class CalloutBlock(BaseBlock):
    type: typing.Literal["callout"] = "callout"
    callout: Callout


class Quote(pydantic.BaseModel):
    rich_text: list[RichText]
    color: Color
    children: list[Block]


class QuoteBlock(BaseBlock):
    type: typing.Literal["quote"] = "quote"
    quote: Quote


class BulletedListItem(pydantic.BaseModel):
    color: Color
    children: list[Block]


class BulletedListItemBlock(BaseBlock):
    type: typing.Literal["bulleted_list_item"] = "bulleted_list_item"
    bulleted_list_item: BulletedListItem


class NumberedListItem(pydantic.BaseModel):
    color: Color
    children: list[Block]


class NumberedListItemBlock(BaseBlock):
    type: typing.Literal["numbered_list_item"] = "numbered_list_item"
    numbered_list_item: NumberedListItem


class Todo(pydantic.BaseModel):
    rich_text: list[RichText]
    checked: bool = False
    color: Color
    children: list[Block]


class TodoBlock(BaseBlock):
    type: typing.Literal["to_do"] = "to_do"
    to_do: Todo


class Toggle(pydantic.BaseModel):
    rich_text: list[RichText]
    color: Color
    children: list[Block]


class ToggleBlock(BaseBlock):
    type: typing.Literal["toggle"] = "toggle"
    toggle: Toggle


class Language(enum.Enum):
    abap = "abap"
    arduino = "arduino"
    bash = "bash"
    basic = "basic"
    c = "c"
    clojure = "clojure"
    coffeescript = "coffeescript"
    cpp = "c++"
    csharp = "c#"
    css = "css"
    dart = "dart"
    diff = "diff"
    docker = "docker"
    elixir = "elixir"
    elm = "elm"
    erlang = "erlang"
    flow = "flow"
    fortran = "fortran"
    fsharp = "f#"
    gherkin = "gherkin"
    glsl = "glsl"
    go = "go"
    graphql = "graphql"
    groovy = "groovy"
    haskell = "haskell"
    html = "html"
    java = "java"
    javascript = "javascript"
    json = "json"
    julia = "julia"
    kotlin = "kotlin"
    latex = "latex"
    less = "less"
    lisp = "lisp"
    livescript = "livescript"
    lua = "lua"
    makefile = "makefile"
    markdown = "markdown"
    markup = "markup"
    matlab = "matlab"
    mermaid = "mermaid"
    nix = "nix"
    objective_c = "objective-c"
    ocaml = "ocaml"
    pascal = "pascal"
    perl = "perl"
    php = "php"
    plain_text = "plain text"
    powershell = "powershell"
    prolog = "prolog"
    protobuf = "protobuf"
    python = "python"
    r = "r"
    reason = "reason"
    ruby = "ruby"
    rust = "rust"
    sass = "sass"
    scala = "scala"
    scheme = "scheme"
    scss = "scss"
    shell = "shell"
    sql = "sql"
    swift = "swift"
    typescript = "typescript"
    vbdotnet = "vb.net"
    verilog = "verilog"
    vhdl = "vhdl"
    visual_basic = "visual basic"
    webassembly = "webassembly"
    xml = "xml"
    yaml = "yaml"
    java_c_cpp_csharp = "java/c/c++/c#"


class Code(pydantic.BaseModel):
    rich_text: list[RichText]
    caption: list[RichText]
    language: Language


class CodeBlock(BaseBlock):
    type: typing.Literal["code"] = "code"
    code: Code


class ChildPage(pydantic.BaseModel):
    title: str


class ChildPageBlock(BaseBlock):
    type: typing.Literal["child_page"] = "child_page"
    child_page: ChildPage


class ChildDatabase(pydantic.BaseModel):
    title: str


class ChildDatabaseBlock(BaseBlock):
    type: typing.Literal["child_database"] = "child_database"
    child_database: ChildDatabase


class Embed(pydantic.BaseModel):
    url: str


class EmbedBlock(BaseBlock):
    type: typing.Literal["embed"] = "embed"
    embed: Embed


class Image(pydantic.BaseModel):
    image: notions.models.file.File


class ImageBlock(BaseBlock):
    type: typing.Literal["image"] = "image"
    image: Image


class Video(pydantic.BaseModel):
    video: notions.models.file.File


class VideoBlock(BaseBlock):
    type: typing.Literal["video"] = "video"
    video: Video


class File(pydantic.BaseModel):
    file: notions.models.file.File
    caption: list[RichText]


class FileBlock(BaseBlock):
    type: typing.Literal["file"] = "file"
    file: File


class Pdf(pydantic.BaseModel):
    pdf: notions.models.file.File


class PdfBlock(BaseBlock):
    type: typing.Literal["pdf"] = "pdf"
    pdf: Pdf


class Bookmark(pydantic.BaseModel):
    url: str
    caption: list[RichText]


class BookmarkBlock(BaseBlock):
    type: typing.Literal["bookmark"] = "bookmark"
    bookmark: Bookmark


class Equation(pydantic.BaseModel):
    expression: str


class EquationBlock(BaseBlock):
    type: typing.Literal["equation"] = "equation"
    equation: Equation


class DividerBlock(BaseBlock):
    type: typing.Literal["divider"] = "divider"


class TableOfContents(pydantic.BaseModel):
    color: Color


class TableOfContentsBlock(BaseBlock):
    type: typing.Literal["table_of_contents"] = "table_of_contents"
    table_of_contents: TableOfContents


class BreadcrumbBlock(BaseBlock):
    type: typing.Literal["breadcrumb"] = "breadcrumb"


class Column(pydantic.BaseModel):
    children: list[Block]


class ColumnBlock(BaseBlock):
    type: typing.Literal["column"] = "column"
    column: Column


class ColumnList(pydantic.BaseModel):
    children: list[ColumnBlock]


class ColumnListBlock(BaseBlock):
    type: typing.Literal["column_list"] = "column_list"
    column_list: ColumnList


class LinkPreview(pydantic.BaseModel):
    url: str


class LinkPreviewBlock(BaseBlock):
    type: typing.Literal["link_preview"] = "link_preview"
    link_preview: LinkPreview


class Template(pydantic.BaseModel):
    rich_text: list[RichText]
    children: list[Block]


class TemplateBlock(BaseBlock):
    type: typing.Literal["template"] = "template"
    template: Template


class LinkToPage(pydantic.BaseModel):
    type: typing.Literal["page_id"]
    page_id: uuid.UUID


class LinkToDatabase(pydantic.BaseModel):
    type: typing.Literal["database_id"]
    database_id: uuid.UUID


class LinkToPageBlock(BaseBlock):
    type: typing.Literal["link_to_page"] = "link_to_page"
    link_to_page: typing.Union[LinkToPage, LinkToDatabase] = pydantic.Field(
        ..., discriminator="type"
    )


BlockType = typing.Union[
    ParagraphBlock,
    Heading1Block,
    Heading2Block,
    Heading3Block,
    CalloutBlock,
    QuoteBlock,
    BulletedListItemBlock,
    NumberedListItemBlock,
    TodoBlock,
    ToggleBlock,
    CodeBlock,
    ChildPageBlock,
    ChildDatabaseBlock,
    EmbedBlock,
    ImageBlock,
    VideoBlock,
    FileBlock,
    PdfBlock,
    BookmarkBlock,
    EquationBlock,
    DividerBlock,
    TableOfContentsBlock,
    BreadcrumbBlock,
    ColumnListBlock,
    ColumnBlock,
]

# Use a pydantic model with a custom root so we can use a custom discriminator on the type
# Faster parsing and nicer errors
class Block(pydantic.BaseModel):
    __root__: BlockType = pydantic.Field(..., discriminator="type")


# Update forward refs for blocks with children
Callout.update_forward_refs()
Quote.update_forward_refs()
BulletedListItem.update_forward_refs()
NumberedListItem.update_forward_refs()
Todo.update_forward_refs()
Toggle.update_forward_refs()
Column.update_forward_refs()
Template.update_forward_refs()
