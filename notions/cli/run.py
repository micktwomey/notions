"""Common run function which does the heavy lifting of formatting output"""

import csv
import enum
import itertools
import logging
import typing

from notions.flatten import flatten_item
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


def json_format_item(
    item: typing.Union[Page, Database],
    output: typing.TextIO,
):
    output.write(flatten_item(item).json())
    output.write("\n")


async def json_format_iterable(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
    formatter=lambda item: flatten_item(item).json(),
):
    items = []
    async for item in iterable:
        items.append(formatter(item))
    output.write("[\n")
    LOG.info(f"Writing {len(items)} items to {output.name}")
    for item in items[0:-1]:
        output.write(item)
        output.write(",\n")
    output.write(items[-1])
    output.write("\n]")


async def notion_json_format_iterable(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
):
    # re-use the json formatter
    await json_format_iterable(iterable, output, formatter=lambda item: item.json())


async def jsonl_format_iterable(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
):
    async for item in iterable:
        output.write(flatten_item(item).json())
        output.write("\n")


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


def yaml_format_item(
    item: typing.Union[Page, Database],
    output: typing.TextIO,
):
    yaml.dump(flatten_item(item).dict(), output)


async def notion_yaml_format_iterable(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
):
    items = []
    async for item in iterable:
        items.append(item.dict())
    yaml.dump(items, output)


async def yaml_format_iterable(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
):
    items = []
    async for item in iterable:
        items.append(flatten_item(item).dict())
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


async def csv_format_iterable(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
    format: str,
    guess_headers: bool,
):
    writer = csv.writer(output, dialect="excel-tab" if format == "tsv" else "excel")
    core_headers = ["type", "id", "title", "created_time", "last_edited_time"]
    first_row = True
    async for item in iterable:
        item = flatten_item(item)
        if first_row:
            if guess_headers:
                # TODO: expand and flatten nested objects to property_nested_name
                property_headers = list(item.properties)
                headers = core_headers + property_headers
            else:
                headers = core_headers
            writer.writerow(headers)
            first_row = False
        row = [item.type, item.id, item.title, item.created_time, item.last_edited_time]
        if guess_headers:
            row += [str(item.properties[header].value) for header in property_headers]
        else:
            row += [str(prop.value) for prop in item.properties.values()]
        writer.writerow(row)


async def csv_format_item(
    item: typing.Union[Page, Database],
    output: typing.TextIO,
    format: str,
    guess_headers: bool,
):
    async def items():
        yield item

    await csv_format_iterable(
        items(), output, format=format, guess_headers=guess_headers
    )


async def run(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
    output_format: OutputFormats,
    text_formatter: typing.Callable[[typing.Any], str] = default_text_formatter,
    guess_headers: bool = False,
):
    """Helper for commands which handles formatting output"""
    if output_format == OutputFormats.notion_json:
        await notion_json_format_iterable(iterable, output)
    elif output_format == OutputFormats.notion_jsonl:
        await notion_jsonl_format_iterable(iterable, output)
    elif output_format == OutputFormats.notion_yaml:
        await notion_yaml_format_iterable(iterable, output)
    elif output_format == OutputFormats.text:
        await text_format_iterable(iterable, output, text_formatter)
    elif output_format == OutputFormats.json:
        await json_format_iterable(iterable, output)
    elif output_format == OutputFormats.jsonl:
        await jsonl_format_iterable(iterable, output)
    elif output_format == OutputFormats.yaml:
        await yaml_format_iterable(iterable, output)
    elif output_format == OutputFormats.tsv:
        await csv_format_iterable(iterable, output, "tsv", guess_headers=guess_headers)
    elif output_format == OutputFormats.csv:
        await csv_format_iterable(iterable, output, "csv", guess_headers=guess_headers)
    else:
        raise NotImplementedError(f"Unknown output format: {output_format=}")


async def run_single_item(
    awaitable: typing.Awaitable[typing.Union[Page, Database]],
    output: typing.TextIO,
    output_format: OutputFormats,
    text_formatter: typing.Callable[[typing.Any], str] = default_text_formatter,
    guess_headers: bool = False,
):
    item = await awaitable
    if output_format == OutputFormats.notion_json:
        notion_json_format_item(item, output)
    elif output_format == OutputFormats.notion_jsonl:
        notion_json_format_item(item, output)
    elif output_format == OutputFormats.notion_yaml:
        notion_yaml_format_item(item, output)
    elif output_format == OutputFormats.text:
        text_format_item(item, output, text_formatter)
    elif output_format == OutputFormats.json:
        json_format_item(item, output)
    elif output_format == OutputFormats.jsonl:
        json_format_item(item, output)
    elif output_format == OutputFormats.yaml:
        yaml_format_item(item, output)
    elif output_format == OutputFormats.tsv:
        await csv_format_item(item, output, "tsv", guess_headers=guess_headers)
    elif output_format == OutputFormats.csv:
        await csv_format_item(item, output, "csv", guess_headers=guess_headers)
    else:
        raise NotImplementedError(f"Unknown output format: {output_format=}")
