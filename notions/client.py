import contextlib

import furl
import httpx

from . import responses


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
                page = responses.PaginatedListResponse.parse_raw(response.content)
                yield page
                has_more = page.has_more
                start_cursor = page.next_cursor

    async def list_databases(self):
        """Performs a GET /databases

        https://developers.notion.com/reference/get-databases
        """
        async for page in self.paginated_request("GET", self.base_url / "v1/databases"):
            for db in page.results:
                yield responses.Database.parse_obj(db)
