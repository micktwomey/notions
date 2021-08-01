import asyncio
import logging
import typing

import coloredlogs
import typer

from notions.client import NotionAsyncClient
from notions.models.request import SearchRequest

from . import database, page
from .api import run_api
from .config import CONFIG, OutputFormats
from .search import run_search

app = typer.Typer()
app.add_typer(database.app, name="database")
app.add_typer(page.app, name="page")

LOG = logging.getLogger(__name__)


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
):
    """Perform an API call with authentication"""
    client = NotionAsyncClient(CONFIG.notion_api_key)
    asyncio.run(
        run_api(
            client,
            method,
            path,
            paginate,
            output=CONFIG.output,
            output_format=CONFIG.output_format,
        )
    )


@app.command()
def search(
    query: typing.Optional[str] = typer.Option(
        None,
        help="When supplied, limits which pages are returned by comparing the query to the page title.",
    )
):
    """Search for pages and databases"""
    client = NotionAsyncClient(CONFIG.notion_api_key)
    asyncio.run(
        run_search(
            client,
            query,
            output=CONFIG.output,
            output_format=CONFIG.output_format,
        )
    )


@app.callback()
def main(
    debug: bool = False,
    verbose: bool = False,
    notion_api_key: str = typer.Option(
        ...,
        envvar="NOTION_API_KEY",
        help=(
            "Notion API key. See https://developers.notion.com/docs/getting-started and https://www.notion.so/my-integrations for how to create a token. "
            "Note that the integration must be added as a user via shared to any database you want to query."
        ),
    ),
    output_format: OutputFormats = typer.Option("text"),
    output: typer.FileTextWrite = typer.Option(
        "-", help="File to write to, defaults to stdout (-)."
    ),
):
    """Notions: a Notion API CLI client"""
    level = "DEBUG" if debug else ("INFO" if verbose else "WARNING")
    coloredlogs.install(level=level)
    CONFIG.notion_api_key = notion_api_key
    CONFIG.output_format = output_format
    CONFIG.output = output

    LOG.debug(f"{CONFIG=}")


if __name__ == "__main__":
    app()
