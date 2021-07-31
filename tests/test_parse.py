import datetime
import json
import uuid

import pydantic

from notions.models.color import Color
from notions.models.database import (
    CreatedTimeProperty,
    Database,
    NumberProperty,
    Properties,
    Select,
    SelectOption,
    SelectProperty,
    TitleProperty,
    URLProperty,
)
from notions.models.number import Number, NumberFormat
from notions.models.parent import WorkspaceParent
from notions.models.rich_text import Annotations, RichTextText, Text

# http https://api.notion.com/v1/databases/cc5ef123-05f5-409e-9b34-38043df965b0 "Notion-Version: 2021-05-13" "Authorization: Bearer $NOTION_API_KEY"| pbcopy
GET_DATABASE_JSON = """
{
    "object": "database",
    "id": "cc5ef123-05f5-409e-9b34-38043df965b0",
    "created_time": "2021-07-12T07:03:00.000Z",
    "last_edited_time": "2021-07-25T22:13:00.000Z",
    "title": [
        {
            "type": "text",
            "text": {
                "content": "Eurorack",
                "link": null
            },
            "annotations": {
                "bold": false,
                "italic": false,
                "strikethrough": false,
                "underline": false,
                "code": false,
                "color": "default"
            },
            "plain_text": "Eurorack",
            "href": null
        }
    ],
    "properties": {
        "Zone": {
            "id": ";vF\\\\",
            "name": "Zone",
            "type": "select",
            "select": {
                "options": [
                    {
                        "id": "999d6839-bc19-4c96-b982-be338a128352",
                        "name": "Rack 1 Bottom",
                        "color": "red"
                    },
                    {
                        "id": "06dced11-bc1e-4df8-99e7-fe9383af8c80",
                        "name": "Rack 1 Top Left",
                        "color": "yellow"
                    }
                ]
            }
        },
        "+12V mA": {
            "id": "J~xw",
            "name": "+12V mA",
            "type": "number",
            "number": {
                "format": "number"
            }
        },
        "Depth (mm)": {
            "id": "a?VV",
            "name": "Depth (mm)",
            "type": "number",
            "number": {
                "format": "number"
            }
        },
        "Created": {
            "id": "gL=>",
            "name": "Created",
            "type": "created_time",
            "created_time": {}
        },
        "Homepage": {
            "id": "gfHx",
            "name": "Homepage",
            "type": "url",
            "url": {}
        },
        "5V mA": {
            "id": "iP{{",
            "name": "5V mA",
            "type": "number",
            "number": {
                "format": "number"
            }
        },
        "-12V mA": {
            "id": "kpdn",
            "name": "-12V mA",
            "type": "number",
            "number": {
                "format": "number"
            }
        },
        "Manufacturer": {
            "id": "nmit",
            "name": "Manufacturer",
            "type": "select",
            "select": {
                "options": [
                    {
                        "id": "85858ee3-1d36-4d61-8e45-90e2d3358464",
                        "name": "Mutable Instruments",
                        "color": "green"
                    },
                    {
                        "id": "ea2042b5-7176-4c7e-ad11-b563b3998754",
                        "name": "ALM Busy Circuits",
                        "color": "brown"
                    },
                    {
                        "id": "44d611d8-62ad-454c-8eae-1bf81624f185",
                        "name": "Intellijel",
                        "color": "purple"
                    }
                ]
            }
        },
        "HP": {
            "id": "uF=u",
            "name": "HP",
            "type": "number",
            "number": {
                "format": "number"
            }
        },
        "Modulargrid": {
            "id": "wt@r",
            "name": "Modulargrid",
            "type": "url",
            "url": {}
        },
        "Name": {
            "id": "title",
            "name": "Name",
            "type": "title",
            "title": {}
        }
    },
    "parent": {
        "type": "workspace",
        "workspace": true
    }
}
"""


def test_parse_get_database():
    db = Database.parse_raw(GET_DATABASE_JSON)
    assert db == Database(
        object="database",
        id=uuid.UUID("cc5ef123-05f5-409e-9b34-38043df965b0"),
        created_time=datetime.datetime(2021, 7, 12, 7, 3, tzinfo=datetime.timezone.utc),
        last_edited_time=datetime.datetime(
            2021, 7, 25, 22, 13, tzinfo=datetime.timezone.utc
        ),
        title=[
            RichTextText(
                type="text",
                plain_text="Eurorack",
                href=None,
                annotations=Annotations(
                    bold=False,
                    italic=False,
                    strikethrough=False,
                    underline=False,
                    code=False,
                    color=Color.default,
                ),
                text=Text(content="Eurorack", link=None),
            )
        ],
        parent=WorkspaceParent(),
        properties={
            "Zone": SelectProperty(
                id=";vF\\",
                name="Zone",
                type="select",
                select=Select(
                    options=[
                        SelectOption(
                            id="999d6839-bc19-4c96-b982-be338a128352",
                            name="Rack 1 Bottom",
                            color=Color.red,
                        ),
                        SelectOption(
                            id="06dced11-bc1e-4df8-99e7-fe9383af8c80",
                            name="Rack 1 Top Left",
                            color=Color.yellow,
                        ),
                    ]
                ),
            ),
            "+12V mA": NumberProperty(
                id="J~xw",
                name="+12V mA",
                type="number",
                number=Number(format=NumberFormat.number),
            ),
            "Depth (mm)": NumberProperty(
                id="a?VV",
                name="Depth (mm)",
                type="number",
                number=Number(format=NumberFormat.number),
            ),
            "Created": CreatedTimeProperty(id="gL=>", name="Created"),
            "Homepage": URLProperty(id="gfHx", name="Homepage"),
            "5V mA": NumberProperty(
                id="iP{{",
                name="5V mA",
                type="number",
                number=Number(format=NumberFormat.number),
            ),
            "-12V mA": NumberProperty(
                id="kpdn",
                name="-12V mA",
                type="number",
                number=Number(format=NumberFormat.number),
            ),
            "Manufacturer": SelectProperty(
                id="nmit",
                name="Manufacturer",
                select=Select(
                    options=[
                        SelectOption(
                            id="85858ee3-1d36-4d61-8e45-90e2d3358464",
                            name="Mutable Instruments",
                            color=Color.green,
                        ),
                        SelectOption(
                            id="ea2042b5-7176-4c7e-ad11-b563b3998754",
                            name="ALM Busy Circuits",
                            color=Color.brown,
                        ),
                        SelectOption(
                            id="44d611d8-62ad-454c-8eae-1bf81624f185",
                            name="Intellijel",
                            color=Color.purple,
                        ),
                    ],
                ),
            ),
            "HP": NumberProperty(
                id="uF=u",
                name="HP",
                type="number",
                number=Number(format=NumberFormat.number),
            ),
            "Modulargrid": URLProperty(id="wt@r", name="Modulargrid"),
            "Name": TitleProperty(id="title", name="Name"),
        },
    )

    assert json.loads(db.json().replace("+00:00", ".000Z")) == json.loads(
        GET_DATABASE_JSON
    )


def test_parse_properties():
    properties_json = """
    {
        "properties": {
            "Zone": {
                "id": ";vF\\\\",
                "name": "Zone",
                "type": "select",
                "select": {
                    "options": [
                        {
                            "id": "999d6839-bc19-4c96-b982-be338a128352",
                            "name": "Rack 1 Bottom",
                            "color": "red"
                        },
                        {
                            "id": "06dced11-bc1e-4df8-99e7-fe9383af8c80",
                            "name": "Rack 1 Top Left",
                            "color": "yellow"
                        }
                    ]
                }
            },
            "+12V mA": {
                "id": "J~xw",
                "name": "+12V mA",
                "type": "number",
                "number": {
                    "format": "number"
                }
            }
        }
    }
    """

    class Props(pydantic.BaseModel):
        properties: Properties

    properties = Props.parse_raw(properties_json)
    assert properties == Props(
        properties={
            "Zone": SelectProperty(
                id=";vF\\",
                name="Zone",
                type="select",
                select=Select(
                    options=[
                        SelectOption(
                            id="999d6839-bc19-4c96-b982-be338a128352",
                            name="Rack 1 Bottom",
                            color=Color.red,
                        ),
                        SelectOption(
                            id="06dced11-bc1e-4df8-99e7-fe9383af8c80",
                            name="Rack 1 Top Left",
                            color=Color.yellow,
                        ),
                    ]
                ),
            ),
            "+12V mA": NumberProperty(
                id="J~xw",
                name="+12V mA",
                type="number",
                number=Number(format=NumberFormat.number),
            ),
        }
    )


def test_parse_number_property():
    number_json = """
    {
        "id": "uF=u",
        "name": "HP",
        "type": "number",
        "number": {
            "format": "number"
        }
    }
    """

    assert NumberProperty.parse_raw(number_json) == NumberProperty(
        id="uF=u",
        name="HP",
        number=Number(format=NumberFormat.number),
    )


def test_parse_select_property():
    select_json = """
    {
        "id": "nmit",
        "name": "Manufacturer",
        "type": "select",
        "select": {
            "options": [
                {
                    "id": "85858ee3-1d36-4d61-8e45-90e2d3358464",
                    "name": "Mutable Instruments",
                    "color": "green"
                },
                {
                    "id": "ea2042b5-7176-4c7e-ad11-b563b3998754",
                    "name": "ALM Busy Circuits",
                    "color": "brown"
                },
                {
                    "id": "44d611d8-62ad-454c-8eae-1bf81624f185",
                    "name": "Intellijel",
                    "color": "purple"
                }
            ]
        }
    }
    """

    assert SelectProperty.parse_raw(select_json) == SelectProperty(
        id="nmit",
        name="Manufacturer",
        select=Select(
            options=[
                SelectOption(
                    id="85858ee3-1d36-4d61-8e45-90e2d3358464",
                    name="Mutable Instruments",
                    color=Color.green,
                ),
                SelectOption(
                    id="ea2042b5-7176-4c7e-ad11-b563b3998754",
                    name="ALM Busy Circuits",
                    color=Color.brown,
                ),
                SelectOption(
                    id="44d611d8-62ad-454c-8eae-1bf81624f185",
                    name="Intellijel",
                    color=Color.purple,
                ),
            ],
        ),
    )


def test_parse_created_time_property():
    created_json = """
    {
        "id": "gL=>",
        "name": "Created",
        "type": "created_time",
        "created_time": {}
    }
    """

    assert CreatedTimeProperty.parse_raw(created_json) == CreatedTimeProperty(
        id="gL=>", name="Created"
    )


def test_parse_url_property():
    url_json = """
    {
        "id": "gfHx",
        "name": "Homepage",
        "type": "url",
        "url": {}
    }
    """

    assert URLProperty.parse_raw(url_json) == URLProperty(id="gfHx", name="Homepage")


def test_parse_title_property():
    title_json = """
    {
        "id": "title",
        "name": "Name",
        "type": "title",
        "title": {}
    }
    """

    assert TitleProperty.parse_raw(title_json) == TitleProperty(id="title", name="Name")
