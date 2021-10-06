import sys
import typing

import typer

from notions.client import NotionAsyncClient
from notions.models.search import Search

from .config import OutputFormats
from .run import run

app = typer.Typer()


async def run_search(
    client: NotionAsyncClient,
    query: typing.Optional[str],
    output: typing.TextIO,
    output_format: OutputFormats,
):
    search_request = Search(query=query)
    await run(client.search(search_request), output=output, output_format=output_format)
