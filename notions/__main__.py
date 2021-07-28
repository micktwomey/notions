import asyncio
import json
import uuid

import colorlog
import typer

from .client import NotionAsyncClient

app = typer.Typer()


async def run_list_databases(client: NotionAsyncClient):
    async for db in client.list_databases():
        print(f"{db.id} : {db.title[0].plain_text} ({db.last_edited_time})")


@app.command()
def list_databases(notion_api_key: str = typer.Argument(..., envvar="NOTION_API_KEY")):
    client = NotionAsyncClient(notion_api_key)
    asyncio.run(run_list_databases(client))


async def run_query_databases(client: NotionAsyncClient, database_id: uuid.UUID):
    async for item in client.query_database(database_id):
        print(item.json())


@app.command()
def query_database(
    database_id: uuid.UUID,
    notion_api_key: str = typer.Argument(..., envvar="NOTION_API_KEY"),
):
    client = NotionAsyncClient(notion_api_key)
    asyncio.run(run_query_databases(client, database_id))


@app.callback()
def main(debug: bool = False, verbose: bool = False):
    level = "DEBUG" if debug else ("INFO" if verbose else "WARNING")
    colorlog.basicConfig(level=level)


if __name__ == "__main__":
    app()
