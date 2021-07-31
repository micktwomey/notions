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


async def text_format(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
    text_formatter: typing.Callable[[typing.Any], str],
):
    async for item in iterable:
        output.write(text_formatter(item))
        output.write("\n")


async def notion_json_format(
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


async def notion_jsonl_format(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
):
    async for item in iterable:
        output.write(item.json())
        output.write("\n")


async def notion_yaml_format(
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
    return f"{item_type} : {item.id} : {title} (last_edited_time={item.last_edited_time.isoformat(' ')})"


async def run(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
    output_format: OutputFormats,
    text_formatter: typing.Callable[[typing.Any], str] = default_text_formatter,
):
    """Helper for commands which handles formatting output"""
    if output_format == OutputFormats.notion_json:
        await notion_json_format(iterable, output)
    elif output_format == OutputFormats.notion_jsonl:
        await notion_jsonl_format(iterable, output)
    elif output_format == OutputFormats.notion_yaml:
        await notion_yaml_format(iterable, output)
    else:
        await text_format(iterable, output, text_formatter)
