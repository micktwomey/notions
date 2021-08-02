"""Example showing basic use of the client for API calls
"""

import asyncio
import os
import typing

import httpx

from notions.client import NotionAsyncClient
from notions.models.database import Database


async def http_list_databases(notion_client: NotionAsyncClient) -> httpx.Response:
    """Do a HTTP call with authentication to list databases

    This uses notions as a convenience for HTTP calls using httpx
    """
    async with notion_client.async_client() as client:
        url = notion_client.get_url_for_path("/v1/databases")
        return await client.request("GET", url.url)


async def list_databases(
    notion_client: NotionAsyncClient,
) -> typing.AsyncIterable[Database]:
    """Do a list db call (automatically reads all pages)

    This is the same underlying call as `http_list_databases` above
    but will also parse the response and handle pagination.

    Will yield notions.models.database.Database
    """
    async for db in notion_client.list_databases():
        yield db


async def main():
    api_token = os.environ.get("NOTION_API_KEY", "no-token-set")
    notion_client = NotionAsyncClient(api_token)

    response = await http_list_databases(notion_client)
    print(response)
    print(response.json())
    response.raise_for_status()

    async for db in list_databases(notion_client):
        print(db.id)
        print(db.title)
        print(db)


if __name__ == "__main__":
    asyncio.run(main())
