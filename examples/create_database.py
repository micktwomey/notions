"""Example showing creating a database with all fields.

This is a fairly verbose example, using all the request and response models.
"""


import asyncio
import logging
import os
import uuid
from datetime import datetime
from decimal import Decimal

from notions.client import NotionAsyncClient
from notions.models import properties
from notions.models.color import Color
from notions.models.database import CreateDatabase, Database
from notions.models.number import Number, NumberFormat
from notions.models.page import CreatePage, CreatePageDatabaseParent, Page, UpdatePage
from notions.models.parent import PageParent
from notions.models.rich_text import Annotations, RichTextText, Text

LOG = logging.getLogger(__name__)


async def create_database(
    client: NotionAsyncClient, parent_page_id: uuid.UUID
) -> Database:
    database_name = f"notions-test {datetime.utcnow().isoformat(' ')}"
    LOG.info(f"Creating database {database_name}")
    create_database_request = CreateDatabase(
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
            "number": properties.CreateDatabaseNumberProperty(
                number=Number(format=NumberFormat.number)
            ),
            "Name": properties.CreateDatabaseTitleProperty(),
        },
    )
    LOG.info(f"Sending request:\n{create_database_request.json(indent=2)}")
    database = await client.create_database(create_database_request)
    LOG.info(f"Got {database=} back")
    return database


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

    if os.environ.get("NOTIONS_KEEP_EXAMPLE_PAGES"):
        LOG.info("NOTIONS_KEEP_EXAMPLE_PAGES set, keeping database")
    else:
        # TODO: delete database
        LOG.info(f"Deleting database {database.id=}")
        LOG.warning(
            "Notion API doesn't support database deletion. You'll have to tidy up yourself! Soz!"
        )


if __name__ == "__main__":
    asyncio.run(main())
