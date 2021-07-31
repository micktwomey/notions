import typing
import uuid

import pydantic


class PersonDetails(pydantic.BaseModel):
    email: str


class Person(pydantic.BaseModel):
    id: uuid.UUID
    object: typing.Literal["user"] = "user"
    name: str
    avatar_url: typing.Optional[str]
    type: typing.Literal["person"] = "person"
    person: PersonDetails


class Bot(pydantic.BaseModel):
    id: uuid.UUID
    object: typing.Literal["user"] = "user"
    name: str
    avatar_url: str
    type: typing.Literal["bot"] = "bot"
    bot: dict


User = typing.Union[Person, Bot]
