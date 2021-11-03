"""File Objects

https://developers.notion.com/reference/file-object
"""

import typing
from datetime import datetime

import pydantic


class ExternalFileDetails(pydantic.BaseModel):
    url: str


class ExternalFile(pydantic.BaseModel):
    name: str
    type: typing.Literal["external"] = "external"
    external: ExternalFileDetails

    def get_value(self):
        return self.external.url


class NotionFileDetails(pydantic.BaseModel):
    url: str
    expiry_time: datetime


class NotionFile(pydantic.BaseModel):
    """Files uploaded to Notion"""

    name: str
    type: typing.Literal["file"] = "file"
    file: NotionFileDetails

    def get_value(self):
        return {
            "url": self.file.url,
            "expiry_time": self.file.expiry_time,
        }


File = typing.Union[ExternalFile, NotionFile]


class PageCover(pydantic.BaseModel):
    """A page's cover, slightly different to a file"""

    type: typing.Literal["external"] = "external"
    external: ExternalFileDetails

    def get_value(self):
        return self.external.url
