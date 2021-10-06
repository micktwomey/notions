import typing

import pydantic


class DatabasePhoneNumberProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["phone_number"] = "phone_number"
    phone_number: dict = pydantic.Field(default_factory=dict)

    def get_value(self):
        return self.phone_number


class PagePhoneNumberProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["phone_number"] = "phone_number"
    phone_number: str

    def get_value(self):
        return self.phone_number
