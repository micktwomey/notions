import typing

import pydantic

from ..user import User


class DatabasePeopleProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["people"] = "people"
    people: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.people


class PagePeopleProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["people"] = "people"
    people: typing.List[User]

    def get_value(self):
        return [person.get_value() for person in self.people]
