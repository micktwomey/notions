import contextlib
import json
import logging
import typing
import uuid

import furl
import httpx

from .models.database import CreateDatabase, Database
from .models.page import CreatePage, Page, UpdatePage
from .models.query_database import QueryDatabase
from .models.response import NotionAPIResponse, PaginatedListResponse
from .models.search import Search

LOG = logging.getLogger(__name__)


class NotionAPIResponseError(Exception):
    def __init__(
        self,
        message: str,
        response: typing.Optional[httpx.Response] = None,
        notion_api_response: typing.Optional[NotionAPIResponse] = None,
    ):
        self.message = message
        self.response = response
        self.notion_api_response = notion_api_response
        super().__init__(message, response, notion_api_response)

    @property
    def has_response(self):
        return self.response is not None

    @property
    def has_notion_api_response(self):
        return self.notion_api_response is not None


class NotionAsyncClient:
    """Async HTTP client for talking to Notion"""

    def __init__(
        self,
        api_token: str,
        base_url="https://api.notion.com/",
        notion_version="2021-08-16",
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

    async def api_request(
        self,
        method: str,
        url: furl.furl,
        json: typing.Any = None,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> NotionAPIResponse:
        """Perform a HTTP request"""
        LOG.debug(f"request: {method=} {url=} {json=}")
        async with self.async_client() as client:
            try:
                response = await client.request(
                    method, url.url, json=json, *args, **kwargs
                )
            except Exception as e:
                raise NotionAPIResponseError(f"Error making request: {e}") from e
            try:
                obj = response.json()
                notion_response = NotionAPIResponse(object=obj["object"], obj=obj)
            except Exception as e:
                raise NotionAPIResponseError(
                    f"Unable to parse response: {e}", response=response
                ) from e

            if response.status_code != 200:
                raise NotionAPIResponseError(
                    f"Non HTTP 200 response: {response.status_code}",
                    response=response,
                    notion_api_response=notion_response,
                )
            return notion_response

    async def paginated_request(
        self,
        method: str,
        url: furl.furl,
        pagination_in_json: bool,
        data: str = None,
        *args: typing.Any,
        **kwargs: typing.Any,
    ):
        """Perform a httpx request, yielding pages"""
        url = url.copy()  # make sure we don't modify the original
        has_more = True
        start_cursor = None
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
            notion_response = await self.api_request(
                method,
                url,
                data=data,
                *args,
                **kwargs,
            )
            LOG.debug(f"{notion_response=}")
            page = notion_response.get_paginated_list_response()
            yield page
            has_more = page.has_more
            start_cursor = page.next_cursor

    async def get_database(self, database_id: uuid.UUID) -> Database:
        """https://developers.notion.com/reference/get-database"""
        response = await self.api_request(
            "GET", self.get_url_for_path("v1/databases", str(database_id))
        )
        return response.get_database()

    async def query_database(
        self, database_id: uuid.UUID, query: QueryDatabase
    ) -> typing.AsyncIterable[Page]:
        """https://developers.notion.com/reference/post-database-query"""
        async for page in self.paginated_request(
            "POST",
            self.base_url / "v1/databases" / str(database_id) / "query",
            data=query.json(exclude_unset=True),
            pagination_in_json=True,
        ):
            for item in page.iter_results():
                LOG.debug(f"{item=}")
                if isinstance(item, Page):
                    yield item
                else:
                    LOG.warning(f"Got unexpected item when querying database: {item=}")

    async def list_databases(self) -> typing.AsyncIterable[Database]:
        """Performs a GET /databases

        https://developers.notion.com/reference/get-databases
        """
        async for page in self.paginated_request(
            "GET", self.base_url / "v1/databases", pagination_in_json=False
        ):
            for item in page.iter_results():
                LOG.debug(f"{item=}")
                if isinstance(item, Database):
                    yield item
                else:
                    LOG.warning(f"Got unexpected item when querying database: {item=}")

    async def create_database(
        self,
        create_database: CreateDatabase,
    ) -> Database:
        """https://developers.notion.com/reference/create-a-database"""
        response = await self.api_request(
            "POST",
            self.get_url_for_path("v1/databases"),
            data=create_database.json(),
        )
        return response.get_database()

    async def get_page(self, page_id: uuid.UUID) -> Page:
        """https://developers.notion.com/reference/get-page"""
        response = await self.api_request(
            "GET", self.get_url_for_path("v1/pages", str(page_id))
        )
        return response.get_page()

    async def create_page(self, create_page: CreatePage) -> Page:
        """https://developers.notion.com/reference/post-page"""
        response = await self.api_request(
            "POST",
            self.get_url_for_path("v1/pages"),
            data=create_page.json(),
        )
        return response.get_page()

    async def update_page(self, page_id: uuid.UUID, update_page: UpdatePage) -> Page:
        """https://developers.notion.com/reference/patch-page"""
        response = await self.api_request(
            "PATCH",
            self.get_url_for_path("v1/pages", str(page_id)),
            data=update_page.json(),
        )
        return response.get_page()

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

    async def search(
        self, search: Search
    ) -> typing.AsyncIterable[typing.Union[Database, Page]]:
        """https://developers.notion.com/reference/post-search"""
        async for page in self.paginated_request(
            "POST",
            self.base_url / "v1/search",
            data=search.json(exclude_unset=True, exclude_none=True),
            pagination_in_json=True,
        ):
            for item in page.iter_results():
                LOG.debug(f"{item=}")
                yield item
