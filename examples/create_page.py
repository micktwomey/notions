"""Example showing page creation, editing and appending children (content)

"""

import asyncio
import logging
import os
import uuid
from decimal import Decimal

from create_database import (  # it's boring re-typing all this, so let's re-use
    create_database,
)

from notions.client import NotionAsyncClient
from notions.models import properties
from notions.models.page import CreatePage, CreatePageDatabaseParent, Page, UpdatePage
from notions.models.rich_text import RichTextText, Text

LOG = logging.getLogger(__name__)


async def create_page(client: NotionAsyncClient, database_id: uuid.UUID) -> Page:
    create_page_request = CreatePage(
        parent=CreatePageDatabaseParent(database_id=database_id),
        children=[],
        properties={
            "Name": properties.CreatePageTitleProperty(
                title=[
                    RichTextText(
                        plain_text="test-page",
                        text=Text(content="test-page"),
                    )
                ]
            ),
            "number": properties.CreatePageNumberProperty(number=Decimal("1.23")),
        },
    )
    LOG.info(f"Sending request:\n{create_page_request.json(indent=2)}")
    page = await client.create_page(create_page_request)
    LOG.info(f"Got {page=} back")
    return page


async def delete_page(client: NotionAsyncClient, page: Page):
    update_page_request = UpdatePage(archived=True, properties=page.properties)
    LOG.info(f"Sending page update request:\n{update_page_request.json(indent=2)}")
    LOG.info(f"Deleting (archiving) page {page.id=}")
    await client.update_page(page.id, update_page_request)


async def main():
    try:
        import coloredlogs  # type: ignore

        coloredlogs.install(level=logging.INFO)
    except ImportError:
        logging.basicConfig(level=logging.INFO)
    api_token = os.environ["NOTION_API_KEY"]
    notions_parent_page_uuid = uuid.UUID(os.environ["NOTIONS_PARENT_PAGE_UUID"])
    notion_client = NotionAsyncClient(api_token)

    database = await create_database(notion_client, notions_parent_page_uuid)
    page = await create_page(notion_client, database_id=database.id)

    LOG.info(f"Getting page back using {page.id=}")
    retrieved_page = await notion_client.get_page(page_id=page.id)
    if page != retrieved_page:
        LOG.warning(
            f"Huh, retrieved page doesn't look like the one we created:\n{page=}\n{retrieved_page=}"
        )
    else:
        LOG.info("Retrieved page looks like one we created!")

    if os.environ.get("NOTIONS_KEEP_EXAMPLE_PAGES"):
        LOG.info("NOTIONS_KEEP_EXAMPLE_PAGES set, keeping pages")
    else:
        await delete_page(client=notion_client, page=page)


if __name__ == "__main__":
    asyncio.run(main())
