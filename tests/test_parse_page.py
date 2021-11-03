import datetime
import decimal
import json
import uuid

from notions.models.color import Color
from notions.models.cover import PageCover
from notions.models.date import DateRange
from notions.models.emoji import EmojiEmoji
from notions.models.file import (
    ExternalFile,
    ExternalFileDetails,
    NotionFile,
    NotionFileDetails,
)
from notions.models.page import Page
from notions.models.parent import DatabaseParent
from notions.models.properties import (
    PageCheckboxProperty,
    PageCreatedByProperty,
    PageCreatedTimeProperty,
    PageDateProperty,
    PageEmailProperty,
    PageFileProperty,
    PageFormulaProperty,
    PageLastEditedByProperty,
    PageLastEditedTimeProperty,
    PageMultiSelectProperty,
    PageNumberProperty,
    PagePeopleProperty,
    PagePhoneNumberProperty,
    PageRelationProperty,
    PageRichTextProperty,
    PageRollupProperty,
    PageSelectProperty,
    PageTitleProperty,
    PageURLProperty,
)
from notions.models.properties.formula import (
    PageBooleanFormula,
    PageDateFormula,
    PageNumberFormula,
    PageStringFormula,
)
from notions.models.properties.multi_select import PageMultiSelectOption
from notions.models.properties.relation import PageRelation
from notions.models.properties.rollup import (
    PageArrayRollup,
    PageDateRollup,
    PageNumberRollup,
    RollupFunction,
)
from notions.models.properties.select import PageSelectOption
from notions.models.rich_text import Annotations, RichText, Text
from notions.models.user import Person, PersonDetails

# Fetch using: notions api GET /v1/pages/ccad10e7-c776-423e-9662-6ad5fb1256d6 | jq . | pbcopy
# Note: I've modified the JSON to format time zones using +00:00 instead of Z.
# It parses either way but it's awkward to verify the roundtrip otherwise.
EXAMPLE_PAGE_JSON = """
{
  "object": "page",
  "id": "ccad10e7-c776-423e-9662-6ad5fb1256d6",
  "created_time": "2021-07-31T17:01:00+00:00",
  "last_edited_time": "2021-10-25T17:31:00+00:00",
  "cover": {
    "type": "external",
    "external": {
      "url": "https://www.notion.so/images/page-cover/nasa_space_shuttle_columbia.jpg"
    }
  },
  "icon": {
    "type": "emoji",
    "emoji": "🤪"
  },
  "parent": {
    "type": "database_id",
    "database_id": "fff51adc-8d4e-414a-a2e3-17e69111c328"
  },
  "archived": false,
  "properties": {
    "Boolean Formula Property": {
      "id": "%3A%3ATX",
      "type": "formula",
      "formula": {
        "type": "boolean",
        "boolean": true
      }
    },
    "Phone property": {
      "id": "%3ACyi",
      "type": "phone_number",
      "phone_number": "+555 1234"
    },
    "URL property": {
      "id": "%3EKRE",
      "type": "url",
      "url": "https://twoistoomany.com/"
    },
    "Person property": {
      "id": "EZD%3B",
      "type": "people",
      "people": [
        {
          "object": "user",
          "id": "b66c20dd-0a48-4418-ae23-2d82ec151be3",
          "name": "Michael Twomey",
          "avatar_url": "https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
          "type": "person",
          "person": {
            "email": "notion@mick.twomeylee.name"
          }
        }
      ]
    },
    "Checkbox property": {
      "id": "L%3C%7D%40",
      "type": "checkbox",
      "checkbox": true
    },
    "Email property": {
      "id": "Mqx%3C",
      "type": "email",
      "email": "test@example.com"
    },
    "Last edited by property": {
      "id": "Q%3En%7C",
      "type": "last_edited_by",
      "last_edited_by": {
        "object": "user",
        "id": "b66c20dd-0a48-4418-ae23-2d82ec151be3",
        "name": "Michael Twomey",
        "avatar_url": "https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
        "type": "person",
        "person": {
          "email": "notion@mick.twomeylee.name"
        }
      }
    },
    "Number Property": {
      "id": "S%3EXJ",
      "type": "number",
      "number": 5.23
    },
    "Muti-select property": {
      "id": "TrTf",
      "type": "multi_select",
      "multi_select": [
        {
          "id": "9eea7e74-5ba3-42fc-9aa3-2a8cfce1a65c",
          "name": "foo",
          "color": "gray"
        },
        {
          "id": "576a716b-c31c-4450-be9d-b804b39654e1",
          "name": "bar",
          "color": "brown"
        }
      ]
    },
    "Relation Property": {
      "id": "_GWY",
      "type": "relation",
      "relation": [
        {
          "id": "ccad10e7-c776-423e-9662-6ad5fb1256d6"
        }
      ]
    },
    "Number Rollup property": {
      "id": "%60%3CGE",
      "type": "rollup",
      "rollup": {
        "type": "number",
        "number": 5.23,
        "function": "sum"
      }
    },
    "File property": {
      "id": "dVLG",
      "type": "files",
      "files": [
        {
          "name": "p8logo.png",
          "type": "file",
          "file": {
            "url": "https://s3.us-west-2.amazonaws.com/secure.notion-static.com/8ebae53f-21ba-4441-b622-95806a8896fa/p8logo.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20211025%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211025T173928Z&X-Amz-Expires=3600&X-Amz-Signature=65a3f9b59d5fa8aca605bae3763415edd26d652a46d7ea8093c06ac4ebd55088&X-Amz-SignedHeaders=host",
            "expiry_time": "2021-10-25T18:39:28.188000+00:00"
          }
        },
        {
          "name": "https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/potw2142a.jpg",
          "type": "external",
          "external": {
            "url": "https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/potw2142a.jpg"
          }
        }
      ]
    },
    "Date property": {
      "id": "eo~%5B",
      "type": "date",
      "date": {
        "start": "2021-07-15",
        "end": null
      }
    },
    "Date Rollup property": {
      "id": "fm%5Dd",
      "type": "rollup",
      "rollup": {
        "type": "date",
        "date": {
          "start": "2021-07-15T00:00:00+00:00",
          "end": "2021-07-15T00:00:00+00:00"
        },
        "function": "date_range"
      }
    },
    "Created by property": {
      "id": "f%7Bol",
      "type": "created_by",
      "created_by": {
        "object": "user",
        "id": "b66c20dd-0a48-4418-ae23-2d82ec151be3",
        "name": "Michael Twomey",
        "avatar_url": "https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
        "type": "person",
        "person": {
          "email": "notion@mick.twomeylee.name"
        }
      }
    },
    "Text property": {
      "id": "keEA",
      "type": "rich_text",
      "rich_text": [
        {
          "type": "text",
          "text": {
            "content": "Foo",
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
          "plain_text": "Foo",
          "href": null
        }
      ]
    },
    "Created Time Property": {
      "id": "l%3BMe",
      "type": "created_time",
      "created_time": "2021-07-31T17:01:00+00:00"
    },
    "String Formula Property": {
      "id": "n%60%7DC",
      "type": "formula",
      "formula": {
        "type": "string",
        "string": "October 25 2021, 17:39"
      }
    },
    "Number Formula property": {
      "id": "oNn%3E",
      "type": "formula",
      "formula": {
        "type": "number",
        "number": 6.23
      }
    },
    "Date Formula Property": {
      "id": "oyUS",
      "type": "formula",
      "formula": {
        "type": "date",
        "date": {
          "start": "2021-10-25T17:39:00+00:00",
          "end": null
        }
      }
    },
    "Email rollup property": {
      "id": "viJS",
      "type": "rollup",
      "rollup": {
        "type": "array",
        "array": [
          {
            "type": "email",
            "email": "test@example.com"
          }
        ],
        "function": "show_original"
      }
    },
    "Last Edited Time Property": {
      "id": "yoI%3D",
      "type": "last_edited_time",
      "last_edited_time": "2021-10-25T17:31:00+00:00"
    },
    "Select property": {
      "id": "%7DXVI",
      "type": "select",
      "select": {
        "id": "6492d7c0-0245-4052-b410-aecc6f882ead",
        "name": "foo",
        "color": "gray"
      }
    },
    "Name": {
      "id": "title",
      "type": "title",
      "title": [
        {
          "type": "text",
          "text": {
            "content": "Fields filled in",
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
          "plain_text": "Fields filled in",
          "href": null
        }
      ]
    }
  },
  "url": "https://www.notion.so/Fields-filled-in-ccad10e7c776423e96626ad5fb1256d6"
}
"""


def test_parse_page_roundtrip():
    assert json.loads(Page.parse_raw(EXAMPLE_PAGE_JSON).json()) == json.loads(
        EXAMPLE_PAGE_JSON
    )


def test_parse_page():
    # Convert to dicts to make pytest diffs easier to read
    assert (
        Page.parse_raw(EXAMPLE_PAGE_JSON).dict()
        == Page(
            id=uuid.UUID("ccad10e7-c776-423e-9662-6ad5fb1256d6"),
            created_time=datetime.datetime(
                2021, 7, 31, 17, 1, 0, tzinfo=datetime.timezone.utc
            ),
            last_edited_time=datetime.datetime(
                2021, 10, 25, 17, 31, 0, tzinfo=datetime.timezone.utc
            ),
            icon=EmojiEmoji(emoji="🤪"),
            cover=PageCover(
                external=ExternalFileDetails(
                    url="https://www.notion.so/images/page-cover/nasa_space_shuttle_columbia.jpg"
                )
            ),
            archived=False,
            properties={
                "Boolean Formula Property": PageFormulaProperty(
                    id="%3A%3ATX", formula=PageBooleanFormula(boolean=True)
                ),
                "Phone property": PagePhoneNumberProperty(
                    id="%3ACyi", phone_number="+555 1234"
                ),
                "URL property": PageURLProperty(
                    id="%3EKRE", url="https://twoistoomany.com/"
                ),
                "Person property": PagePeopleProperty(
                    id="EZD%3B",
                    people=[
                        Person(
                            id=uuid.UUID("b66c20dd-0a48-4418-ae23-2d82ec151be3"),
                            name="Michael Twomey",
                            avatar_url="https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
                            person=PersonDetails(email="notion@mick.twomeylee.name"),
                        )
                    ],
                ),
                "Checkbox property": PageCheckboxProperty(
                    id="L%3C%7D%40", checkbox=True
                ),
                "Email property": PageEmailProperty(
                    id="Mqx%3C", email="test@example.com"
                ),
                "Last edited by property": PageLastEditedByProperty(
                    id="Q%3En%7C",
                    last_edited_by=Person(
                        id=uuid.UUID("b66c20dd-0a48-4418-ae23-2d82ec151be3"),
                        name="Michael Twomey",
                        avatar_url="https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
                        person=PersonDetails(email="notion@mick.twomeylee.name"),
                    ),
                ),
                "Number Property": PageNumberProperty(
                    id="S%3EXJ", number=decimal.Decimal("5.23")
                ),
                "Muti-select property": PageMultiSelectProperty(
                    id="TrTf",
                    multi_select=[
                        PageMultiSelectOption(
                            id=uuid.UUID("9eea7e74-5ba3-42fc-9aa3-2a8cfce1a65c"),
                            name="foo",
                            color=Color.gray,
                        ),
                        PageMultiSelectOption(
                            id=uuid.UUID("576a716b-c31c-4450-be9d-b804b39654e1"),
                            name="bar",
                            color=Color.brown,
                        ),
                    ],
                ),
                "Relation Property": PageRelationProperty(
                    id="_GWY",
                    relation=[
                        PageRelation(
                            id=uuid.UUID("ccad10e7-c776-423e-9662-6ad5fb1256d6")
                        )
                    ],
                ),
                "Number Rollup property": PageRollupProperty(
                    id="%60%3CGE",
                    rollup=PageNumberRollup(
                        number=decimal.Decimal("5.23"), function=RollupFunction.sum
                    ),
                ),
                "File property": PageFileProperty(
                    id="dVLG",
                    files=[
                        NotionFile(
                            name="p8logo.png",
                            file=NotionFileDetails(
                                url="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/8ebae53f-21ba-4441-b622-95806a8896fa/p8logo.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20211025%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211025T173928Z&X-Amz-Expires=3600&X-Amz-Signature=65a3f9b59d5fa8aca605bae3763415edd26d652a46d7ea8093c06ac4ebd55088&X-Amz-SignedHeaders=host",
                                expiry_time=datetime.datetime(
                                    2021,
                                    10,
                                    25,
                                    18,
                                    39,
                                    28,
                                    188000,
                                    tzinfo=datetime.timezone.utc,
                                ),
                            ),
                        ),
                        ExternalFile(
                            name="https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/potw2142a.jpg",
                            external=ExternalFileDetails(
                                url="https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/potw2142a.jpg"
                            ),
                        ),
                    ],
                ),
                "Date property": PageDateProperty(
                    id="eo~%5B", date=DateRange(start=datetime.date(2021, 7, 15))
                ),
                "Date Rollup property": PageRollupProperty(
                    id="fm%5Dd",
                    rollup=PageDateRollup(
                        date=DateRange(
                            start=datetime.datetime(
                                2021, 7, 15, 0, 0, tzinfo=datetime.timezone.utc
                            ),
                            end=datetime.datetime(
                                2021, 7, 15, 0, 0, tzinfo=datetime.timezone.utc
                            ),
                        ),
                        function=RollupFunction.date_range,
                    ),
                ),
                "Created by property": PageCreatedByProperty(
                    id="f%7Bol",
                    created_by=Person(
                        id=uuid.UUID("b66c20dd-0a48-4418-ae23-2d82ec151be3"),
                        name="Michael Twomey",
                        avatar_url="https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
                        person=PersonDetails(email="notion@mick.twomeylee.name"),
                    ),
                ),
                "Text property": PageRichTextProperty(
                    id="keEA",
                    rich_text=[
                        RichText(
                            type="text",
                            plain_text="Foo",
                            annotations=Annotations(
                                bold=False,
                                italic=False,
                                strikethrough=False,
                                underline=False,
                                code=False,
                                color="default",
                            ),
                            text=Text(content="Foo"),
                        )
                    ],
                ),
                "Created Time Property": PageCreatedTimeProperty(
                    id="l%3BMe",
                    created_time=datetime.datetime(
                        2021, 7, 31, 17, 1, 0, tzinfo=datetime.timezone.utc
                    ),
                ),
                "String Formula Property": PageFormulaProperty(
                    id="n%60%7DC",
                    formula=PageStringFormula(string="October 25 2021, 17:39"),
                ),
                "Number Formula property": PageFormulaProperty(
                    id="oNn%3E",
                    formula=PageNumberFormula(number=decimal.Decimal("6.23")),
                ),
                "Date Formula Property": PageFormulaProperty(
                    id="oyUS",
                    formula=PageDateFormula(
                        date=DateRange(
                            start=datetime.datetime(
                                2021, 10, 25, 17, 39, tzinfo=datetime.timezone.utc
                            ),
                        )
                    ),
                ),
                "Email rollup property": PageRollupProperty(
                    id="viJS",
                    rollup=PageArrayRollup(
                        array=[{"type": "email", "email": "test@example.com"}],
                        function=RollupFunction.show_original,
                    ),
                ),
                "Last Edited Time Property": PageLastEditedTimeProperty(
                    id="yoI%3D",
                    last_edited_time=datetime.datetime(
                        2021, 10, 25, 17, 31, 0, tzinfo=datetime.timezone.utc
                    ),
                ),
                "Select property": PageSelectProperty(
                    id="%7DXVI",
                    select=PageSelectOption(
                        id=uuid.UUID("6492d7c0-0245-4052-b410-aecc6f882ead"),
                        name="foo",
                        color=Color.gray,
                    ),
                ),
                "Name": PageTitleProperty(
                    id="title",
                    title=[
                        RichText(
                            type="text",
                            plain_text="Fields filled in",
                            annotations=Annotations(
                                bold=False,
                                italic=False,
                                strikethrough=False,
                                underline=False,
                                code=False,
                                color="default",
                            ),
                            text=Text(content="Fields filled in"),
                        )
                    ],
                ),
            },
            parent=DatabaseParent(
                database_id=uuid.UUID("fff51adc-8d4e-414a-a2e3-17e69111c328")
            ),
            url="https://www.notion.so/Fields-filled-in-ccad10e7c776423e96626ad5fb1256d6",
        ).dict()
    )


def test_parse_3d_printer_page():
    """Test parsing a particular failing page from my Notion"""
    raw_obj = {
        "object": "page",
        "id": "18e7c11d-6f26-4817-ae56-3a1fb845d4c5",
        "created_time": "2021-07-28T14:44:00.000Z",
        "last_edited_time": "2021-07-30T14:38:00.000Z",
        "cover": {
            "type": "external",
            "external": {
                "url": "https://media.prusaprinters.org/media/prints/3673/stls/158818_1b8490e9-887d-4b11-b219-0c68d3e0d026/thumbs/cover/180x180/png/prusa_mmu_enclosure_11_black_preview.png"
            },
        },
        "icon": None,
        "parent": {
            "type": "database_id",
            "database_id": "2bbd3201-5dfa-4045-8b5c-310ea3e46ae3",
        },
        "archived": False,
        "properties": {
            "Group": {
                "id": "ABBR",
                "type": "select",
                "select": {
                    "id": "0a34eb46-2f0d-4f6a-95a8-de7c3fa5578d",
                    "name": "PSU",
                    "color": "yellow",
                },
            },
            "Expected Duration Hours": {
                "id": "Aa%7C%5E",
                "type": "number",
                "number": 5,
            },
            "Material Usage (g)": {"id": "D_hH", "type": "number", "number": 79},
            "Project": {"id": "I%60yX", "type": "relation", "relation": []},
            "Material": {
                "id": "R%3BGB",
                "type": "select",
                "select": {
                    "id": "592c100c-f3ec-4baa-a5d4-7791a781ba69",
                    "name": "PETG",
                    "color": "brown",
                },
            },
            "Stage": {"id": "YZQS", "type": "select", "select": None},
            "Expected Duration Minutes": {
                "id": "cHV%7B",
                "type": "number",
                "number": 23,
            },
            "Description": {
                "id": "sNYl",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Black PSU mount", "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "Black PSU mount",
                        "href": None,
                    }
                ],
            },
            "Name": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "prusa_mmu_enclosure_11_black_02mm_pet_mk3s_5h23.gcode",
                            "link": None,
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "prusa_mmu_enclosure_11_black_02mm_pet_mk3s_5h23.gcode",
                        "href": None,
                    }
                ],
            },
        },
        "url": "https://www.notion.so/prusa_mmu_enclosure_11_black_02mm_pet_mk3s_5h23-gcode-18e7c11d6f264817ae563a1fb845d4c5",
    }
    page = Page.parse_obj(raw_obj)
    assert page.id == uuid.UUID("18e7c11d-6f26-4817-ae56-3a1fb845d4c5")


def test_parse_turing_machine_page():
    raw_obj = {
        "object": "page",
        "id": "bbcb80cb-83ae-489e-b1bb-8074b64636dd",
        "created_time": "2021-09-09T19:37:00.000Z",
        "last_edited_time": "2021-09-09T19:38:00.000Z",
        "cover": None,
        "icon": None,
        "parent": {
            "type": "database_id",
            "database_id": "cc5ef123-05f5-409e-9b34-38043df965b0",
        },
        "archived": False,
        "properties": {
            "Zone": {
                "id": "%3BvF%5C",
                "type": "select",
                "select": {
                    "id": "999d6839-bc19-4c96-b982-be338a128352",
                    "name": "Rack 1 Bottom",
                    "color": "red",
                },
            },
            "+12V mA": {"id": "J~xw", "type": "number", "number": None},
            "Depth (mm)": {"id": "a%3FVV", "type": "number", "number": 38},
            "Created": {
                "id": "gL%3D%3E",
                "type": "created_time",
                "created_time": "2021-09-09T19:37:00.000Z",
            },
            "Homepage": {"id": "gfHx", "type": "url", "url": None},
            "5V mA": {"id": "iP%7B%7B", "type": "number", "number": None},
            "-12V mA": {"id": "kpdn", "type": "number", "number": None},
            "Manufacturer": {
                "id": "nmit",
                "type": "select",
                "select": {
                    "id": "dae51df7-8de4-4f82-874d-c93f5e8d3409",
                    "name": "Music Thing Modular",
                    "color": "pink",
                },
            },
            "HP": {"id": "uF%3Du", "type": "number", "number": 10},
            "Modulargrid": {
                "id": "wt%40r",
                "type": "url",
                "url": "https://www.modulargrid.net/e/music-thing-modular-turing-machine-mk-ii--",
            },
            "Name": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {"content": "Turing Machine MK II", "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "Turing Machine MK II",
                        "href": None,
                    }
                ],
            },
        },
        "url": "https://www.notion.so/Turing-Machine-MK-II-bbcb80cb83ae489eb1bb8074b64636dd",
    }
    page = Page.parse_obj(raw_obj)
    assert page.id == uuid.UUID("bbcb80cb-83ae-489e-b1bb-8074b64636dd")


def test_parse_example_page():
    raw_obj = {
        "object": "page",
        "id": "ccad10e7-c776-423e-9662-6ad5fb1256d6",
        "created_time": "2021-07-31T17:01:00.000Z",
        "last_edited_time": "2021-07-31T18:31:00.000Z",
        "cover": None,
        "icon": None,
        "parent": {
            "type": "database_id",
            "database_id": "fff51adc-8d4e-414a-a2e3-17e69111c328",
        },
        "archived": False,
        "properties": {
            "Boolean Formula Property": {
                "id": "%3A%3ATX",
                "type": "formula",
                "formula": {"type": "boolean", "boolean": True},
            },
            "Phone property": {
                "id": "%3ACyi",
                "type": "phone_number",
                "phone_number": "+555 1234",
            },
            "URL property": {
                "id": "%3EKRE",
                "type": "url",
                "url": "https://twoistoomany.com/",
            },
            "Person property": {
                "id": "EZD%3B",
                "type": "people",
                "people": [
                    {
                        "object": "user",
                        "id": "b66c20dd-0a48-4418-ae23-2d82ec151be3",
                        "name": "Michael Twomey",
                        "avatar_url": "https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
                        "type": "person",
                        "person": {"email": "notion@mick.twomeylee.name"},
                    }
                ],
            },
            "Checkbox property": {
                "id": "L%3C%7D%40",
                "type": "checkbox",
                "checkbox": True,
            },
            "Email property": {
                "id": "Mqx%3C",
                "type": "email",
                "email": "test@example.com",
            },
            "Last edited by property": {
                "id": "Q%3En%7C",
                "type": "last_edited_by",
                "last_edited_by": {
                    "object": "user",
                    "id": "b66c20dd-0a48-4418-ae23-2d82ec151be3",
                    "name": "Michael Twomey",
                    "avatar_url": "https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
                    "type": "person",
                    "person": {"email": "notion@mick.twomeylee.name"},
                },
            },
            "Number Property": {"id": "S%3EXJ", "type": "number", "number": 5.23},
            "Muti-select property": {
                "id": "TrTf",
                "type": "multi_select",
                "multi_select": [
                    {
                        "id": "9eea7e74-5ba3-42fc-9aa3-2a8cfce1a65c",
                        "name": "foo",
                        "color": "gray",
                    },
                    {
                        "id": "576a716b-c31c-4450-be9d-b804b39654e1",
                        "name": "bar",
                        "color": "brown",
                    },
                ],
            },
            "Relation Property": {
                "id": "_GWY",
                "type": "relation",
                "relation": [{"id": "ccad10e7-c776-423e-9662-6ad5fb1256d6"}],
            },
            "Number Rollup property": {
                "id": "%60%3CGE",
                "type": "rollup",
                "rollup": {"type": "number", "number": 5.23, "function": "sum"},
            },
            "File property": {
                "id": "dVLG",
                "type": "files",
                "files": [
                    {
                        "name": "p8logo.png",
                        "type": "file",
                        "file": {
                            "url": "https://s3.us-west-2.amazonaws.com/secure.notion-static.com/8ebae53f-21ba-4441-b622-95806a8896fa/p8logo.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20211007%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211007T161838Z&X-Amz-Expires=3600&X-Amz-Signature=5a9331f4ffba5230e1f1345af270debfb0dd0765941304022d3c9d965e8ac1ec&X-Amz-SignedHeaders=host",
                            "expiry_time": "2021-10-07T17:18:38.930Z",
                        },
                    }
                ],
            },
            "Date property": {
                "id": "eo~%5B",
                "type": "date",
                "date": {"start": "2021-07-15", "end": None},
            },
            "Date Rollup property": {
                "id": "fm%5Dd",
                "type": "rollup",
                "rollup": {
                    "type": "date",
                    "date": {
                        "start": "2021-07-15T00:00:00+00:00",
                        "end": "2021-07-15T00:00:00+00:00",
                    },
                    "function": "date_range",
                },
            },
            "Created by property": {
                "id": "f%7Bol",
                "type": "created_by",
                "created_by": {
                    "object": "user",
                    "id": "b66c20dd-0a48-4418-ae23-2d82ec151be3",
                    "name": "Michael Twomey",
                    "avatar_url": "https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
                    "type": "person",
                    "person": {"email": "notion@mick.twomeylee.name"},
                },
            },
            "Text property": {
                "id": "keEA",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Foo", "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "Foo",
                        "href": None,
                    }
                ],
            },
            "Created Time Property": {
                "id": "l%3BMe",
                "type": "created_time",
                "created_time": "2021-07-31T17:01:00.000Z",
            },
            "String Formula Property": {
                "id": "n%60%7DC",
                "type": "formula",
                "formula": {"type": "string", "string": "October 7 2021, 16:18"},
            },
            "Number Formula property": {
                "id": "oNn%3E",
                "type": "formula",
                "formula": {"type": "number", "number": 6.23},
            },
            "Date Formula Property": {
                "id": "oyUS",
                "type": "formula",
                "formula": {
                    "type": "date",
                    "date": {"start": "2021-10-07T16:18:00+00:00", "end": None},
                },
            },
            "Email rollup property": {
                "id": "viJS",
                "type": "rollup",
                "rollup": {
                    "type": "array",
                    "array": [{"type": "email", "email": "test@example.com"}],
                    "function": "show_original",
                },
            },
            "Last Edited Time Property": {
                "id": "yoI%3D",
                "type": "last_edited_time",
                "last_edited_time": "2021-07-31T18:31:00.000Z",
            },
            "Select property": {
                "id": "%7DXVI",
                "type": "select",
                "select": {
                    "id": "6492d7c0-0245-4052-b410-aecc6f882ead",
                    "name": "foo",
                    "color": "gray",
                },
            },
            "Name": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {"content": "Fields filled in", "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "Fields filled in",
                        "href": None,
                    }
                ],
            },
        },
        "url": "https://www.notion.so/Fields-filled-in-ccad10e7c776423e96626ad5fb1256d6",
    }
    page = Page.parse_obj(raw_obj)
    assert page.id == uuid.UUID("ccad10e7-c776-423e-9662-6ad5fb1256d6")
