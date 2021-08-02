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

    def get_value(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": "person",
            "avatar_url": self.avatar_url,
            "email": self.person.email,
            "is_bot": False,
        }


class Bot(pydantic.BaseModel):
    id: uuid.UUID
    object: typing.Literal["user"] = "user"
    name: str
    avatar_url: str
    type: typing.Literal["bot"] = "bot"
    bot: dict

    def get_value(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": "bot",
            "avatar_url": self.avatar_url,
            "email": None,
            "is_bot": True,
        }


User = typing.Union[Person, Bot]
