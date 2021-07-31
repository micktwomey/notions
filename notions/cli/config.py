import dataclasses
import enum
import sys
import typing


class OutputFormats(enum.Enum):
    text = "text"
    json = "json"
    jsonl = "jsonl"
    yaml = "yaml"


@dataclasses.dataclass
class Config:
    """Simple global config for sharing from typer callback to commands"""

    input: typing.Optional[typing.TextIO] = None
    output: typing.TextIO = sys.stdout
    notion_api_key: str = "no-key-set"
    output_format: OutputFormats = OutputFormats.text


CONFIG = Config()
