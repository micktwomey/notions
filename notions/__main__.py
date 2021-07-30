import asyncio
import dataclasses
import json
import logging
import typing
import uuid

import coloredlogs
import typer

from .client import NotionAsyncClient
from .models.request import QueryDatabaseRequest, SearchRequest

app = typer.Typer()

LOG = logging.getLogger(__name__)


@dataclasses.dataclass
class Config:
    notion_api_key: str


CONFIG = Config(notion_api_key="unset")


async def run_list_databases(client: NotionAsyncClient):
    async for db in client.list_databases():
        print(f"{db.id} : {db.title[0].plain_text} ({db.last_edited_time})")


@app.command()
def list_databases():
    """List available databases"""
    client = NotionAsyncClient(CONFIG.notion_api_key)
    asyncio.run(run_list_databases(client))


async def run_query_databases(client: NotionAsyncClient, database_id: uuid.UUID):
    query = QueryDatabaseRequest(filter={}, sorts=[])
    async for item in client.query_database(database_id, query):
        print(item.json())


@app.command()
def query_database(
    database_id: uuid.UUID,
):
    """Query a database for pages"""
    client = NotionAsyncClient(CONFIG.notion_api_key)
    asyncio.run(run_query_databases(client, database_id))


async def run_api(
    client: NotionAsyncClient,
    method: str,
    path: str,
    paginated: bool,
    input: typing.Optional[typing.BinaryIO],
    output: typing.BinaryIO,
):
    url = client.get_url_for_path(path)
    if paginated:
        async for page in client.paginated_request(
            method, url, pagination_in_json=False
        ):
            for item in page.results:
                output.write(item.json().encode("utf-8"))
    else:
        response = await client.request(method, url)
        output.write(response.content)


@app.command()
def api(
    method: str = typer.Argument("GET", help="HTTP method, defaults to GET."),
    path: str = typer.Argument(
        ...,
        help="Path to request (use full path, i.e. include /v1 portion at beginning).",
    ),
    paginate: bool = typer.Option(
        False, help="Process paginated results, printing one JSON per line."
    ),
    input: typing.Optional[typer.FileBinaryRead] = typer.Argument(
        None, help="File to read from, use - for stdin."
    ),
    output: typer.FileBinaryWrite = typer.Argument(
        "-", help="File to write to, defaults to stdout (-)."
    ),
):
    """Perform an API call with authentication"""
    client = NotionAsyncClient(CONFIG.notion_api_key)
    asyncio.run(run_api(client, method, path, paginate, input, output))


async def run_search(client: NotionAsyncClient, query: typing.Optional[str]):
    search_request = SearchRequest(query=query)
    async for item in client.search(search_request):
        print(item.json())


@app.command()
def search(
    query: str = typer.Option(
        "",
        help="When supplied, limits which pages are returned by comparing the query to the page title.",
    )
):
    """Search for pages and databases"""
    client = NotionAsyncClient(CONFIG.notion_api_key)
    asyncio.run(run_search(client, query))


@app.callback()
def main(
    debug: bool = False,
    verbose: bool = False,
    notion_api_key: str = typer.Option(..., envvar="NOTION_API_KEY"),
):
    """Notions: a Notion API CLI client"""
    level = "DEBUG" if debug else ("INFO" if verbose else "WARNING")
    coloredlogs.install(level=level)
    CONFIG.notion_api_key = notion_api_key

    LOG.debug(f"{CONFIG=}")


if __name__ == "__main__":
    app()
