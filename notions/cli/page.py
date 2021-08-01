import asyncio
import sys
import typing
import uuid

import typer

from notions.client import NotionAsyncClient

from .config import CONFIG, OutputFormats
from .run import run, run_single_item

app = typer.Typer()


async def run_get_page(
    client: NotionAsyncClient,
    output: typing.TextIO,
    output_format: OutputFormats,
    page_id: uuid.UUID,
):
    await run_single_item(
        client.get_page(page_id=page_id),
        output=output,
        output_format=output_format,
    )


@app.command("get")
def get_page(
    page_id: uuid.UUID = typer.Argument(..., help="The ID of the page to get"),
):
    """Get a single page"""
    client = NotionAsyncClient(CONFIG.notion_api_key)
    asyncio.run(
        run_get_page(
            client,
            output=CONFIG.output,
            output_format=CONFIG.output_format,
            page_id=page_id,
        )
    )
