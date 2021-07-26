import asyncio
import uuid
import typer

from .client import NotionAsyncClient

app = typer.Typer()


async def run_list_databases(client: NotionAsyncClient):
    async for db in client.list_databases():
        print(db.json())


@app.command()
def list_databases(notion_api_key: str = typer.Argument(..., envvar="NOTION_API_KEY")):
    client = NotionAsyncClient(notion_api_key)
    asyncio.run(run_list_databases(client))


if __name__ == "__main__":
    app()
