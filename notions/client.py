import contextlib
import json
import logging
import typing
import uuid

import furl
import httpx

from .models.database import Database
from .models.page import Page
from .models.request import (
    CreateDatabaseRequest,
    CreatePageRequest,
    QueryDatabaseRequest,
    SearchRequest,
)
from .models.response import PaginatedListResponse
from .models.update import UpdatePageRequest

LOG = logging.getLogger(__name__)


class NotionAsyncClient:
    """Async HTTP client for talking to Notion"""

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
        """Append path segments to the base url"""
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
                "Content-Type": "application/json",
            },
        ) as httpx_client:
            yield httpx_client

    async def request(
        self,
        method: str,
        url: furl.furl,
        raise_for_status=True,
        json: typing.Any = None,
        *args,
        **kwargs,
    ):
        """Perform a HTTP request"""
        LOG.debug(f"request: {method=} {url=} {json=}")
        async with self.async_client() as client:
            response = await client.request(method, url.url, json=json, *args, **kwargs)
            if raise_for_status:
                response.raise_for_status()
            return response

    async def paginated_request(
        self,
        method: str,
        url: furl.furl,
        pagination_in_json: bool,
        raise_for_status=True,
        data: str = None,
        *args,
        **kwargs,
    ):
        """Perform a httpx request, yielding pages"""
        url = url.copy()
        has_more = True
        start_cursor = None
        async with self.async_client() as client:
            while has_more:
                if start_cursor is not None:
                    # start_cursor is set either in the json body or the query params, depending on the request
                    if pagination_in_json:
                        LOG.debug(f"Setting {start_cursor=} in JSON body")
                        # Since the data is already encoded by pydantic, load, update and re-encode it
                        request_json = json.loads(data)
                        request_json["start_cursor"] = start_cursor
                        data = json.dumps(request_json)
                    else:
                        LOG.debug(f"Setting {start_cursor=} in url params")
                        url.set({"start_cursor": start_cursor})
                LOG.debug(f"paginated_request: {method=} {url=} {data=}")
                response = await client.request(
                    method, url.url, data=data, *args, **kwargs
                )
                LOG.debug(f"{response.content=}")
                if raise_for_status:
                    response.raise_for_status()
                page = PaginatedListResponse.parse_raw(response.content)
                yield page
                has_more = page.has_more
                start_cursor = page.next_cursor

    async def get_database(self, database_id: uuid.UUID) -> Database:
        """https://developers.notion.com/reference/get-database"""
        raise NotImplementedError()

    async def query_database(
        self, database_id: uuid.UUID, query: QueryDatabaseRequest
    ) -> typing.AsyncIterable[Page]:
        """https://developers.notion.com/reference/post-database-query"""
        async for page in self.paginated_request(
            "POST",
            self.base_url / "v1/databases" / str(database_id) / "query",
            data=query.json(exclude_unset=True),
            pagination_in_json=True,
        ):
            for item in page.results:
                LOG.debug(f"{item=}")
                yield item

    async def list_databases(self) -> typing.AsyncIterable[Database]:
        """Performs a GET /databases

        https://developers.notion.com/reference/get-databases
        """
        async for page in self.paginated_request(
            "GET", self.base_url / "v1/databases", pagination_in_json=False
        ):
            for db in page.results:
                LOG.debug(f"{db=}")
                yield db

    async def create_database(
        self,
        database: CreateDatabaseRequest,
    ) -> Database:
        """https://developers.notion.com/reference/create-a-database"""
        raise NotImplementedError()

    async def get_page(self, page_id: uuid.UUID) -> Page:
        """https://developers.notion.com/reference/get-page"""
        response = await self.request(
            "GET", self.get_url_for_path("v1/pages", str(page_id))
        )
        return Page.parse_raw(response.content)

    async def create_page(self, page: CreatePageRequest) -> Page:
        """https://developers.notion.com/reference/post-page"""
        raise NotImplementedError()

    async def update_page(self, page_id: uuid.UUID, page: UpdatePageRequest) -> Page:
        """https://developers.notion.com/reference/patch-page"""
        raise NotImplementedError()

    async def get_block_children(self, block_id: uuid.UUID):
        """https://developers.notion.com/reference/get-block-children"""
        raise NotImplementedError()

    async def append_block_children(self, block_id: uuid.UUID, children: list):
        """https://developers.notion.com/reference/patch-block-children"""
        raise NotImplementedError()

    async def get_user(self, user_id: uuid.UUID):
        """https://developers.notion.com/reference/get-user"""
        raise NotImplementedError()

    async def list_all_users(
        self,
    ):
        """https://developers.notion.com/reference/get-users"""
        raise NotImplementedError()

    async def search(self, search_request: SearchRequest):
        """https://developers.notion.com/reference/post-search"""
        async for page in self.paginated_request(
            "POST",
            self.base_url / "v1/search",
            data=search_request.json(exclude_unset=True, exclude_none=True),
            pagination_in_json=True,
        ):
            for item in page.results:
                LOG.debug(f"{item=}")
                yield item
