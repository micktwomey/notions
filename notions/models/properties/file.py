import typing

import pydantic

from ..file import File


class DatabaseFileProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["files"] = "files"
    files: typing.Dict

    def get_value(self):
        return self.files


class PageFileProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["files"] = "files"
    files: typing.List[File]

    def get_value(self):
        return [f.get_value() for f in self.files]
