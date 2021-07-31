import asyncio
import typing

import furl
import typer

from notions.client import NotionAsyncClient

from .config import OutputFormats
from .run import run

app = typer.Typer()


async def paginated_request(client: NotionAsyncClient, method: str, url: furl.furl):
    async for page in client.paginated_request(method, url, pagination_in_json=False):
        for item in page.results:
            yield item


async def run_api(
    client: NotionAsyncClient,
    method: str,
    path: str,
    paginated: bool,
    output: typing.TextIO,
    output_format: OutputFormats,
):
    url = client.get_url_for_path(path)
    if paginated:
        await run(
            paginated_request(client, method, url),
            output=output,
            output_format=output_format,
        )
    else:
        response = await client.request(method, url)
        output.write(response.content.decode("UTF-8"))
