import asyncio
import sys
import typing
import uuid

import typer

from notions.client import NotionAsyncClient
from notions.models.request import QueryDatabaseRequest, QueryDatabaseSort

from . import yaml
from .config import CONFIG, OutputFormats
from .run import run

app = typer.Typer()


async def run_list_databases(
    client: NotionAsyncClient, output: typing.TextIO, output_format: OutputFormats
):
    await run(
        client.list_databases(),
        output=output,
        output_format=output_format,
    )


@app.command("list")
def list_databases():
    """List available databases"""
    client = NotionAsyncClient(CONFIG.notion_api_key)
    asyncio.run(
        run_list_databases(
            client, output=CONFIG.output, output_format=CONFIG.output_format
        )
    )


async def run_query_databases(
    client: NotionAsyncClient,
    database_id: uuid.UUID,
    output: typing.TextIO,
    output_format: OutputFormats,
    sorts: typing.List[typing.List[str]],
):
    query_sorts = []
    for sort in sorts:
        if len(sort) == 1:
            query_sorts.append(
                QueryDatabaseSort(property=sort[0], direction="ascending")
            )
        elif len(sort) == 2:
            query_sorts.append(QueryDatabaseSort(property=sort[0], direction=sort[1]))
        else:
            raise ValueError(f"Invalid sort: {sort=}")
    query = QueryDatabaseRequest(sorts=query_sorts)
    await run(
        client.query_database(database_id, query),
        output=output,
        output_format=output_format,
    )


@app.command("query")
def query_database(
    database_id: uuid.UUID,
    sort_properties: typing.List[str] = typer.Option(
        [],
        "--sort-property",
        help=(
            "A property to sort on. "
            "Optional: specify direction with property:[ascending|descending]. "
            "e.g. title:ascending. "
            "Can be specified multiple times. "
        ),
    ),
):
    """Query a database for pages"""
    client = NotionAsyncClient(CONFIG.notion_api_key)
    asyncio.run(
        run_query_databases(
            client,
            database_id,
            output=CONFIG.output,
            output_format=CONFIG.output_format,
            sorts=[p.split(":", 1) for p in sort_properties],
        )
    )
