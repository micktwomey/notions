import contextlib
import logging
import typing
import uuid
from os import path

import furl
import httpx

from .models.database import Database
from .models.page import Page
from .models.response import PaginatedListResponse

LOG = logging.getLogger(__name__)


class NotionAsyncClient:
    def __init__(
        self,
        api_token: str,
        base_url="https://api.notion.com/",
        notion_version="2021-05-13",
    ):
        self.api_token = api_token
        self.base_url = furl.furl(base_url)
        self.notion_version = notion_version

    def get_url_for_path(self, *path_segments: str) -> furl.furl:
        url = self.base_url.copy()
        for segment in path_segments:
            url = url / segment
        return url

    @contextlib.asynccontextmanager
    async def async_client(self):
        """Context manager giving a httpx.AsyncClient set up for requests"""
        async with httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Notion-Version": self.notion_version,
            },
        ) as httpx_client:
            yield httpx_client

    async def request(
        self, method: str, url: furl.furl, raise_for_status=True, *args, **kwargs
    ):
        async with self.async_client() as client:
            response = await client.request(method, url.url, *args, **kwargs)
            if raise_for_status:
                response.raise_for_status()
            return response

    async def paginated_request(
        self, method: str, url: furl.furl, raise_for_status=True, *args, **kwargs
    ):
        """Perform a httpx request, yielding pages"""
        url = url.copy()
        has_more = True
        start_cursor = None
        async with self.async_client() as client:
            while has_more:
                if start_cursor is not None:
                    url.set({"start_cursor": start_cursor})
                response = await client.request(method, url.url, *args, **kwargs)
                if raise_for_status:
                    response.raise_for_status()
                LOG.debug(f"{response.content=}")
                page = PaginatedListResponse.parse_raw(response.content)
                yield page
                has_more = page.has_more
                start_cursor = page.next_cursor

    async def list_databases(self) -> typing.AsyncIterable[Database]:
        """Performs a GET /databases

        https://developers.notion.com/reference/get-databases
        """
        async for page in self.paginated_request("GET", self.base_url / "v1/databases"):
            for db in page.results:
                LOG.debug(db)
                yield Database.parse_obj(db)

    async def query_database(self, database_id: uuid.UUID):
        """https://developers.notion.com/reference/post-database-query"""
        async for page in self.paginated_request(
            "POST", self.base_url / "v1/databases" / str(database_id) / "query"
        ):
            for item in page.results:
                LOG.debug(item)
                yield Page.parse_obj(item)
