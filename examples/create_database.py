"""Example showing creating a database with all fields, inserting a page and retrieving

This is a fairly verbose example, using all the request and response models.
"""


import asyncio
import logging
import os
import uuid
from datetime import datetime
from decimal import Decimal

from notions.client import NotionAsyncClient
from notions.models.color import Color
from notions.models.database import Database
from notions.models.number import Number, NumberFormat
from notions.models.page import Page
from notions.models.parent import PageParent
from notions.models.request import (
    CreateDatabaseRequest,
    CreatePageDatabaseParent,
    CreatePageRequest,
    DatabaseNumberProperty,
    DatabaseTitleProperty,
    PageNumberProperty,
    PageTitleProperty,
)
from notions.models.rich_text import Annotations, RichTextText, Text
from notions.models.update import UpdatePageRequest

LOG = logging.getLogger(__name__)


async def create_database(
    client: NotionAsyncClient, parent_page_id: uuid.UUID
) -> Database:
    database_name = f"notions-test {datetime.utcnow().isoformat(' ')}"
    LOG.info(f"Creating databsae {database_name}")
    create_database_request = CreateDatabaseRequest(
        parent=PageParent(page_id=parent_page_id),
        title=[
            RichTextText(
                plain_text=database_name,
                text=Text(content=database_name),
                annotations=Annotations(
                    bold=False,
                    italic=False,
                    strikethrough=False,
                    underline=False,
                    code=False,
                    color=Color.default,
                ),
            )
        ],
        properties={
            "number": DatabaseNumberProperty(number=Number(format=NumberFormat.number)),
            "Name": DatabaseTitleProperty(),
        },
    )
    LOG.info(f"Sending request:\n{create_database_request.json(indent=2)}")
    database = await client.create_database(create_database_request)
    LOG.info(f"Got {database=} back")
    return database


async def create_page(client: NotionAsyncClient, database_id: uuid.UUID) -> Page:
    create_page_request = CreatePageRequest(
        parent=CreatePageDatabaseParent(database_id=database_id),
        children=[],
        properties={
            "Name": PageTitleProperty(
                title=[
                    RichTextText(
                        plain_text="test-page",
                        text=Text(content="test-page"),
                        annotations=Annotations(
                            bold=False,
                            italic=False,
                            strikethrough=False,
                            underline=False,
                            code=False,
                            color=Color.default,
                        ),
                    )
                ]
            ),
            "number": PageNumberProperty(number=Decimal("1.23")),
        },
    )
    LOG.info(f"Sending request:\n{create_page_request.json(indent=2)}")
    page = await client.create_page(create_page_request)
    LOG.info(f"Got {page=} back")
    return page


async def main():
    try:
        import coloredlogs

        coloredlogs.install(level=logging.INFO)
    except ImportError:
        logging.basicConfig(level=logging.INFO)
    api_token = os.environ["NOTION_API_KEY"]
    notions_parent_page_uuid = os.environ["NOTIONS_PARENT_PAGE_UUID"]
    notion_client = NotionAsyncClient(api_token)

    database = await create_database(notion_client, uuid.UUID(notions_parent_page_uuid))

    LOG.info(f"Getting database back using {database.id=}")
    retrieved_database = await notion_client.get_database(database_id=database.id)
    if database != retrieved_database:
        LOG.warning(
            f"Huh, retrieved database doesn't look like the one we created:\n{database=}\n{retrieved_database=}"
        )
    else:
        LOG.info("Retrieved database looks like one we created!")

    page = await create_page(notion_client, database.id)

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
        update_page_request = UpdatePageRequest(
            archived=True, properties=page.properties
        )
        LOG.info(f"Sending page update request:\n{update_page_request.json(indent=2)}")
        LOG.info(f"Deleting (archiving) page {page.id=}")
        await notion_client.update_page(page.id, update_page_request)

        # TODO: delete database
        LOG.info(f"Deleting database {database.id=}")
        LOG.warning(
            "Notion API doesn't support database deletion. You'll have to tidy up yourself! Soz!"
        )


if __name__ == "__main__":
    asyncio.run(main())
