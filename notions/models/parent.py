import typing
import uuid

import pydantic


class PageParent(pydantic.BaseModel):
    type: typing.Literal["page_id"]
    page_id: uuid.UUID

    def get_value(self):
        return self.page_id


class WorkspaceParent(pydantic.BaseModel):
    type: typing.Literal["workspace"] = "workspace"
    workspace: typing.Literal[True] = True

    def get_value(self):
        return self.workspace


class DatabaseParent(pydantic.BaseModel):
    type: typing.Literal["database_id"] = "database_id"
    database_id: uuid.UUID

    def get_value(self):
        return self.database_id


# Each content type has slightly different valid parents
AllParents = typing.Union[PageParent, WorkspaceParent, DatabaseParent]
DatabaseParents = typing.Union[PageParent, WorkspaceParent]
PageParents = typing.Union[PageParent, DatabaseParent]
