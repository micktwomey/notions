"""Flatten down Notion data structures to a simpler representation

"""
import datetime
import decimal
import re
import typing
import uuid

import pydantic

import notions.models.color
import notions.models.database
import notions.models.page
from notions.models.parent import DatabaseParent

Key = typing.NewType("Key", str)


class Property(pydantic.BaseModel):
    key: Key
    name: str
    type: str
    value: typing.Any


class FlatPage(pydantic.BaseModel):
    """Simpler representation of Notion data

    Properties are keyed off a programming language friendly key instead of a full string.

    Where possible properties are massively simplified to aid templating.

    The Name title property is also promoted to a first class attribute (with just the plain text).
    """

    type: typing.Literal["page"] = "page"
    id: uuid.UUID
    created_time: datetime.datetime
    last_edited_time: datetime.datetime
    archived: bool
    properties: typing.Dict[Key, Property]
    parent: typing.Any
    parent_type: str
    url: str
    name: str


def keyify(name: str) -> Key:
    replaced = re.sub("[^0-9a-z]+", "_", name.lower().strip())
    if re.match(r"^[a-z]+", replaced) is not None:
        return Key(replaced)
    # Add a leading underscore to give better odds of this being a valid language identifier
    return Key("_" + replaced)


def flatten_page(page: notions.models.page.Page) -> FlatPage:
    properties = {}
    for property_name, property in page.properties.items():
        key = keyify(property_name)
        properties[key] = Property(
            key=key,
            name=property_name,
            type=property.type,
            value=property.get_value(),
        )
    return FlatPage(
        id=page.id,
        created_time=page.created_time,
        last_edited_time=page.last_edited_time,
        archived=page.archived,
        properties=properties,
        parent_type=page.parent.type,
        parent=page.parent.get_value(),
        url=page.url,
        name=properties[Key("name")].value if "name" in properties else "",
    )


class FlatDatabase(pydantic.BaseModel):
    type: typing.Literal["database"] = "database"
    id: uuid.UUID
    created_time: datetime.datetime
    last_edited_time: datetime.datetime
    title: str
    parent: typing.Any
    parent_type: str
    properties: typing.Dict[Key, Property]


def flatten_database(database: notions.models.database.Database) -> FlatDatabase:
    properties = {}
    for property_name, property in database.properties.items():
        key = keyify(property_name)
        properties[key] = Property(
            key=key,
            name=property_name,
            type=property.type,
            value=property.get_value(),
        )
    titles = [t.get_value() for t in database.title]
    titles = [t for t in titles if t]
    return FlatDatabase(
        id=database.id,
        created_time=database.created_time,
        last_edited_time=database.last_edited_time,
        properties=properties,
        parent_type=database.parent.type,
        parent=database.parent.get_value(),
        title=titles[0] if titles else "",
    )


def flatten_item(
    item: typing.Union[notions.models.database.Database, notions.models.page.Page]
) -> typing.Union[FlatDatabase, FlatPage]:
    if isinstance(item, notions.models.database.Database):
        return flatten_database(item)
    if isinstance(item, notions.models.page.Page):
        return flatten_page(item)
    raise NotImplementedError(f"Unsupported item type {item=}")
