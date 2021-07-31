"""YAML dumping helpers

Handle the various data types we defined in notions.
"""

import decimal
import typing
import uuid

import yaml

from notions.models.color import Color
from notions.models.number import NumberFormat


# From https://github.com/yaml/pyyaml/issues/103
class NoAliasDumper(yaml.Dumper):
    """Dumper with automatic aliases disabled"""

    def ignore_aliases(self, data):
        return True


def uuid_yaml_representer(dumper: yaml.Dumper, data: uuid.UUID):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))


NoAliasDumper.add_representer(uuid.UUID, uuid_yaml_representer)


def color_yaml_representer(dumper: yaml.Dumper, data: Color):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data.value)


NoAliasDumper.add_representer(Color, color_yaml_representer)


def number_format_yaml_representer(dumper: yaml.Dumper, data: NumberFormat):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data.value)


NoAliasDumper.add_representer(NumberFormat, number_format_yaml_representer)


def decimal_yaml_representer(dumper: yaml.Dumper, data: decimal.Decimal):
    tag = "tag:yaml.org,2002:float"
    value = str(data)
    # If we don't do this we get a nasty `!!float '28'`
    if "." not in value:
        tag = "tag:yaml.org,2002:int"
    return dumper.represent_scalar(tag, value)


NoAliasDumper.add_representer(decimal.Decimal, decimal_yaml_representer)


def dump(obj: typing.Any, stream: typing.TextIO):
    """Dump to YAML"""
    yaml.dump(obj, stream, Dumper=NoAliasDumper)
