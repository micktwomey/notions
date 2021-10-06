import typing

import pydantic


class DatabaseFilesProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["files"] = "files"
    files: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.files


class PageFilesProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["files"] = "files"
    files: typing.List[typing.Dict[str, str]]

    def get_value(self):
        return self.files
