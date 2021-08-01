"""Common run function which does the heavy lifting of formatting output"""

import enum
import itertools
import logging
import typing

from notions.models.database import Database
from notions.models.page import Page, PageTitleProperty

from . import yaml
from .config import OutputFormats

LOG = logging.getLogger(__name__)


def text_format_item(
    item: typing.Union[Page, Database],
    output: typing.TextIO,
    text_formatter: typing.Callable[[typing.Any], str],
):
    output.write(text_formatter(item))
    output.write("\n")


async def text_format_iterable(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
    text_formatter: typing.Callable[[typing.Any], str],
):
    async for item in iterable:
        text_format_item(item, output, text_formatter)


def notion_json_format_item(
    item: typing.Union[Page, Database],
    output: typing.TextIO,
):
    output.write(item.json())
    output.write("\n")


async def notion_json_format_iterable(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
):
    items = []
    async for item in iterable:
        items.append(item.json())
    output.write("[\n")
    LOG.info(f"Writing {len(items)} items to {output.name}")
    for item in items[0:-1]:
        output.write(item)
        output.write(",\n")
    output.write(items[-1])
    output.write("\n]")


async def notion_jsonl_format_iterable(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
):
    async for item in iterable:
        output.write(item.json())
        output.write("\n")


def notion_yaml_format_item(
    item: typing.Union[Page, Database],
    output: typing.TextIO,
):
    yaml.dump(item.dict(), output)


async def notion_yaml_format_iterable(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
):
    items = []
    async for item in iterable:
        items.append(item.dict())
    yaml.dump(items, output)


def default_text_formatter(item: typing.Union[Database, Page]) -> str:
    title = "-No title-"
    item_type = "unknown"
    if isinstance(item, Database):
        title_property = item.title
        item_type = "database"
    else:
        item_type = "page"
        if "Name" in item.properties and isinstance(
            item.properties["Name"], PageTitleProperty
        ):
            title_property = item.properties["Name"].title

    titles = [t.plain_text for t in title_property]
    if titles:
        title = titles[0]
    return f"{item_type} : {item.id} : {title} : {list(item.properties)}"


async def run(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
    output_format: OutputFormats,
    text_formatter: typing.Callable[[typing.Any], str] = default_text_formatter,
):
    """Helper for commands which handles formatting output"""
    if output_format == OutputFormats.notion_json:
        await notion_json_format_iterable(iterable, output)
    elif output_format == OutputFormats.notion_jsonl:
        await notion_jsonl_format_iterable(iterable, output)
    elif output_format == OutputFormats.notion_yaml:
        await notion_yaml_format_iterable(iterable, output)
    else:
        await text_format_iterable(iterable, output, text_formatter)


async def run_single_item(
    awaitable: typing.Awaitable[typing.Union[Page, Database]],
    output: typing.TextIO,
    output_format: OutputFormats,
    text_formatter: typing.Callable[[typing.Any], str] = default_text_formatter,
):
    item = await awaitable
    if output_format == OutputFormats.notion_json:
        notion_json_format_item(item, output)
    elif output_format == OutputFormats.notion_jsonl:
        notion_json_format_item(item, output)
    elif output_format == OutputFormats.notion_yaml:
        notion_yaml_format_item(item, output)
    else:
        text_format_item(item, output, text_formatter)
