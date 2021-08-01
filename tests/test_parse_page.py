import datetime
import decimal
import json
import uuid

from notions.models.color import Color
from notions.models.page import (
    ArrayRollup,
    BooleanFormula,
    DateFormula,
    DateRange,
    DateRollup,
    MultiSelectOption,
    NumberFormula,
    NumberRollup,
    Page,
    PageCheckboxProperty,
    PageCreatedByProperty,
    PageCreatedTimeProperty,
    PageDateProperty,
    PageEmailProperty,
    PageFilesProperty,
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
    Relation,
    SelectOption,
    StringFormula,
)
from notions.models.parent import DatabaseParent
from notions.models.rich_text import Annotations, RichText, RichTextText, Text
from notions.models.user import Person, PersonDetails

# Note: I've modified the JSON to format time zones using +00:00 instead of Z.
# It parses either way but it's awkward to verify the roundtrip otherwise.
EXAMPLE_PAGE_JSON = """
{
  "object": "page",
  "id": "ccad10e7-c776-423e-9662-6ad5fb1256d6",
  "created_time": "2021-07-31T17:01:00+00:00",
  "last_edited_time": "2021-07-31T18:31:00+00:00",
  "parent": {
    "type": "database_id",
    "database_id": "fff51adc-8d4e-414a-a2e3-17e69111c328"
  },
  "archived": false,
  "properties": {
    "Boolean Formula Property": {
      "id": "::TX",
      "type": "formula",
      "formula": {
        "type": "boolean",
        "boolean": true
      }
    },
    "Phone property": {
      "id": ":Cyi",
      "type": "phone_number",
      "phone_number": "+555 1234"
    },
    "URL property": {
      "id": ">KRE",
      "type": "url",
      "url": "https://twoistoomany.com/"
    },
    "Person property": {
      "id": "EZD;",
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
      "id": "L<}@",
      "type": "checkbox",
      "checkbox": true
    },
    "Email property": {
      "id": "Mqx<",
      "type": "email",
      "email": "test@example.com"
    },
    "Last edited by property": {
      "id": "Q>n|",
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
      "id": "S>XJ",
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
      "id": "`<GE",
      "type": "rollup",
      "rollup": {
        "type": "number",
        "number": 5.23
      }
    },
    "File property": {
      "id": "dVLG",
      "type": "files",
      "files": [
        {
          "name": "p8logo.png"
        }
      ]
    },
    "Date property": {
      "id": "eo~[",
      "type": "date",
      "date": {
        "start": "2021-07-15",
        "end": null
      }
    },
    "Date Rollup property": {
      "id": "fm]d",
      "type": "rollup",
      "rollup": {
        "type": "date",
        "date": {
          "start": "2021-07-15T00:00:00+00:00",
          "end": "2021-07-15T00:00:00+00:00"
        }
      }
    },
    "Created by property": {
      "id": "f{ol",
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
      "id": "l;Me",
      "type": "created_time",
      "created_time": "2021-07-31T17:01:00+00:00"
    },
    "String Formula Property": {
      "id": "n`}C",
      "type": "formula",
      "formula": {
        "type": "string",
        "string": "July 31 2021, 23:46"
      }
    },
    "Number Formula property": {
      "id": "oNn>",
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
          "start": "2021-07-31T23:46:00+00:00",
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
        ]
      }
    },
    "Last Edited Time Property": {
      "id": "yoI=",
      "type": "last_edited_time",
      "last_edited_time": "2021-07-31T18:31:00+00:00"
    },
    "Select property": {
      "id": "}XVI",
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
                2021, 7, 31, 18, 31, 0, tzinfo=datetime.timezone.utc
            ),
            archived=False,
            properties={
                "Boolean Formula Property": PageFormulaProperty(
                    id="::TX", formula=BooleanFormula(boolean=True)
                ),
                "Phone property": PagePhoneNumberProperty(
                    id=":Cyi", phone_number="+555 1234"
                ),
                "URL property": PageURLProperty(
                    id=">KRE", url="https://twoistoomany.com/"
                ),
                "Person property": PagePeopleProperty(
                    id="EZD;",
                    people=[
                        Person(
                            id=uuid.UUID("b66c20dd-0a48-4418-ae23-2d82ec151be3"),
                            name="Michael Twomey",
                            avatar_url="https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
                            person=PersonDetails(email="notion@mick.twomeylee.name"),
                        )
                    ],
                ),
                "Checkbox property": PageCheckboxProperty(id="L<}@", checkbox=True),
                "Email property": PageEmailProperty(
                    id="Mqx<", email="test@example.com"
                ),
                "Last edited by property": PageLastEditedByProperty(
                    id="Q>n|",
                    last_edited_by=Person(
                        id=uuid.UUID("b66c20dd-0a48-4418-ae23-2d82ec151be3"),
                        name="Michael Twomey",
                        avatar_url="https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
                        person=PersonDetails(email="notion@mick.twomeylee.name"),
                    ),
                ),
                "Number Property": PageNumberProperty(
                    id="S>XJ", number=decimal.Decimal("5.23")
                ),
                "Muti-select property": PageMultiSelectProperty(
                    id="TrTf",
                    multi_select=[
                        MultiSelectOption(
                            id=uuid.UUID("9eea7e74-5ba3-42fc-9aa3-2a8cfce1a65c"),
                            name="foo",
                            color=Color.gray,
                        ),
                        MultiSelectOption(
                            id=uuid.UUID("576a716b-c31c-4450-be9d-b804b39654e1"),
                            name="bar",
                            color=Color.brown,
                        ),
                    ],
                ),
                "Relation Property": PageRelationProperty(
                    id="_GWY",
                    relation=[
                        Relation(id=uuid.UUID("ccad10e7-c776-423e-9662-6ad5fb1256d6"))
                    ],
                ),
                "Number Rollup property": PageRollupProperty(
                    id="`<GE", rollup=NumberRollup(number=decimal.Decimal("5.23"))
                ),
                "File property": PageFilesProperty(
                    id="dVLG", files=[{"name": "p8logo.png"}]
                ),
                "Date property": PageDateProperty(
                    id="eo~[", date=DateRange(start=datetime.date(2021, 7, 15))
                ),
                "Date Rollup property": PageRollupProperty(
                    id="fm]d",
                    rollup=DateRollup(
                        date=DateRange(
                            start=datetime.datetime(
                                2021, 7, 15, 0, 0, tzinfo=datetime.timezone.utc
                            ),
                            end=datetime.datetime(
                                2021, 7, 15, 0, 0, tzinfo=datetime.timezone.utc
                            ),
                        )
                    ),
                ),
                "Created by property": PageCreatedByProperty(
                    id="f{ol",
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
                    id="l;Me",
                    created_time=datetime.datetime(
                        2021, 7, 31, 17, 1, 0, tzinfo=datetime.timezone.utc
                    ),
                ),
                "String Formula Property": PageFormulaProperty(
                    id="n`}C", formula=StringFormula(string="July 31 2021, 23:46")
                ),
                "Number Formula property": PageFormulaProperty(
                    id="oNn>", formula=NumberFormula(number=decimal.Decimal("6.23"))
                ),
                "Date Formula Property": PageFormulaProperty(
                    id="oyUS",
                    formula=DateFormula(
                        date=DateRange(
                            start=datetime.datetime(
                                2021, 7, 31, 23, 46, tzinfo=datetime.timezone.utc
                            ),
                        )
                    ),
                ),
                "Email rollup property": PageRollupProperty(
                    id="viJS",
                    rollup=ArrayRollup(
                        array=[{"type": "email", "email": "test@example.com"}]
                    ),
                ),
                "Last Edited Time Property": PageLastEditedTimeProperty(
                    id="yoI=",
                    last_edited_time=datetime.datetime(
                        2021, 7, 31, 18, 31, 0, tzinfo=datetime.timezone.utc
                    ),
                ),
                "Select property": PageSelectProperty(
                    id="}XVI",
                    select=SelectOption(
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
