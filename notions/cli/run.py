"""Common run function which does the heavy lifting of formatting output"""

import enum
import itertools
import logging
import typing

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


async def json_format(
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


async def jsonl_format(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
):
    async for item in iterable:
        output.write(item.json())
        output.write("\n")


async def yaml_format(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
):
    items = []
    async for item in iterable:
        items.append(item.dict())
    yaml.dump(items, output)


async def run(
    iterable: typing.AsyncIterable,
    output: typing.TextIO,
    output_format: OutputFormats,
    text_formatter: typing.Callable[[typing.Any], str] = lambda item: f"{item=}",
):
    """Helper for commands which handles formatting output"""
    if output_format == OutputFormats.json:
        await json_format(iterable, output)
    elif output_format == OutputFormats.jsonl:
        await jsonl_format(iterable, output)
    elif output_format == OutputFormats.yaml:
        await yaml_format(iterable, output)
    else:
        await text_format(iterable, output, text_formatter)
