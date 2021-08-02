import asyncio
import os

from notions.client import NotionAsyncClient


async def main():
    api_token = os.environ.get("NOTION_API_KEY", "no-token-set")
    notion_client = NotionAsyncClient(api_token)

    # Do a straight HTTP call with authentication
    async with notion_client.async_client() as client:
        url = notion_client.get_url_for_path("/v1/databases")
        response = await client.request("GET", url.url)
        print(response)
        print(response.json())
        response.raise_for_status()

    # Do a list db call (automatically reads all pages)
    # Will give you a notions.models.database.Database
    async for db in notion_client.list_databases():
        print(db.id)
        print(db.title)
        print(db)


if __name__ == "__main__":
    asyncio.run(main())
