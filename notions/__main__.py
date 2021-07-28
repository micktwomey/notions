import asyncio
import io
import json
import sys
import typing
import uuid

import colorlog
import typer

from .client import NotionAsyncClient

app = typer.Typer()


async def run_list_databases(client: NotionAsyncClient):
    async for db in client.list_databases():
        print(f"{db.id} : {db.title[0].plain_text} ({db.last_edited_time})")


@app.command()
def list_databases(notion_api_key: str = typer.Option(..., envvar="NOTION_API_KEY")):
    """List available databases"""
    client = NotionAsyncClient(notion_api_key)
    asyncio.run(run_list_databases(client))


async def run_query_databases(client: NotionAsyncClient, database_id: uuid.UUID):
    async for item in client.query_database(database_id):
        print(item.json())


@app.command()
def query_database(
    database_id: uuid.UUID,
    notion_api_key: str = typer.Option(..., envvar="NOTION_API_KEY"),
):
    """Query a database for pages"""
    client = NotionAsyncClient(notion_api_key)
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
        async for page in client.paginated_request(method, url):
            for item in page.results:
                output.write(json.dumps(item).encode("utf-8"))
    else:
        response = await client.request(method, url)
        output.write(response.content)


@app.command()
def api(
    notion_api_key: str = typer.Option(..., envvar="NOTION_API_KEY"),
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
    client = NotionAsyncClient(notion_api_key)
    asyncio.run(run_api(client, method, path, paginate, input, output))


@app.callback()
def main(debug: bool = False, verbose: bool = False):
    """Notion API CLI Client"""
    level = "DEBUG" if debug else ("INFO" if verbose else "WARNING")
    colorlog.basicConfig(level=level)


if __name__ == "__main__":
    app()
