import json

from notions.models.page import Page

EXAMPLE_PAGE = {
    "object": "page",
    "id": "490788c8-8da9-4277-ac78-508675e1390e",
    "created_time": "2021-07-12T07:03:00.000Z",
    "last_edited_time": "2021-07-25T22:11:00.000Z",
    "parent": {
        "type": "database_id",
        "database_id": "cc5ef123-05f5-409e-9b34-38043df965b0",
    },
    "archived": False,
    "properties": {
        "Zone": {
            "id": ";vF\\",
            "type": "select",
            "select": {
                "id": "06dced11-bc1e-4df8-99e7-fe9383af8c80",
                "name": "Rack 1 Top Left",
                "color": "yellow",
            },
        },
        "+12V mA": {"id": "J~xw", "type": "number", "number": 50},
        "Depth (mm)": {"id": "a?VV", "type": "number", "number": 32},
        "Created": {
            "id": "gL=>",
            "type": "created_time",
            "created_time": "2021-07-12T07:03:00.000Z",
        },
        "Homepage": {
            "id": "gfHx",
            "type": "url",
            "url": "https://busycircuits.com/alm017/",
        },
        "5V mA": {"id": "iP{{", "type": "number", "number": 0},
        "-12V mA": {"id": "kpdn", "type": "number", "number": 1},
        "Manufacturer": {
            "id": "nmit",
            "type": "select",
            "select": {
                "id": "ea2042b5-7176-4c7e-ad11-b563b3998754",
                "name": "ALM Busy Circuits",
                "color": "brown",
            },
        },
        "HP": {"id": "uF=u", "type": "number", "number": 8},
        "Modulargrid": {
            "id": "wt@r",
            "type": "url",
            "url": "https://www.modulargrid.net/e/alm-busy-circuits-alm017-pamela-s-new-workout",
        },
        "Name": {
            "id": "title",
            "type": "title",
            "title": [
                {
                    "type": "text",
                    "text": {"content": "ALM017 - Pamela's NEW Workout", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "ALM017 - Pamela's NEW Workout",
                    "href": None,
                }
            ],
        },
    },
    "url": "https://www.notion.so/ALM017-Pamela-s-NEW-Workout-490788c88da94277ac78508675e1390e",
}


def test_page():
    assert (
        json.loads(Page.parse_obj(EXAMPLE_PAGE).json().replace("+00:00", ".000Z"))
        == EXAMPLE_PAGE
    )
