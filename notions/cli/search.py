import sys
import typing

import typer

from notions.client import NotionAsyncClient
from notions.models.request import SearchRequest

from .config import OutputFormats
from .run import run

app = typer.Typer()


async def run_search(
    client: NotionAsyncClient,
    query: typing.Optional[str],
    output: typing.TextIO,
    output_format: OutputFormats,
):
    search_request = SearchRequest(query=query)
    await run(client.search(search_request), output=output, output_format=output_format)
