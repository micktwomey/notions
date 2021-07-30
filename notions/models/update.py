import pydantic

from .page import PageProperties


class UpdatePageRequest(pydantic.BaseModel):
    properties: PageProperties
    archived: bool = False
