import typing

import pydantic


class EmojiEmoji(pydantic.BaseModel):
    type: typing.Literal["emoji"] = "emoji"
    emoji: str


Emoji = typing.Union[EmojiEmoji]
