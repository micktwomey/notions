import datetime
import decimal
import json
import uuid

from notions.flatten import flatten_database, flatten_item, flatten_page
from notions.models.database import Database
from notions.models.page import Page

from .test_parse_database import EXAMPLE_DATABASE_JSON
from .test_parse_page import EXAMPLE_PAGE_JSON

EXAMPLE_FLAT_PAGE = {
    "id": uuid.UUID("ccad10e7-c776-423e-9662-6ad5fb1256d6"),
    "created_time": datetime.datetime(2021, 7, 31, 17, 1, tzinfo=datetime.timezone.utc),
    "last_edited_time": datetime.datetime(
        2021, 7, 31, 18, 31, tzinfo=datetime.timezone.utc
    ),
    "archived": False,
    "properties": {
        "boolean_formula_property": {
            "key": "boolean_formula_property",
            "name": "Boolean Formula Property",
            "type": "formula",
            "value": True,
        },
        "phone_property": {
            "key": "phone_property",
            "name": "Phone property",
            "type": "phone_number",
            "value": "+555 1234",
        },
        "url_property": {
            "key": "url_property",
            "name": "URL property",
            "type": "url",
            "value": "https://twoistoomany.com/",
        },
        "person_property": {
            "key": "person_property",
            "name": "Person property",
            "type": "people",
            "value": [
                {
                    "id": uuid.UUID("b66c20dd-0a48-4418-ae23-2d82ec151be3"),
                    "name": "Michael Twomey",
                    "type": "person",
                    "avatar_url": "https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
                    "email": "notion@mick.twomeylee.name",
                    "is_bot": False,
                }
            ],
        },
        "checkbox_property": {
            "key": "checkbox_property",
            "name": "Checkbox property",
            "type": "checkbox",
            "value": True,
        },
        "email_property": {
            "key": "email_property",
            "name": "Email property",
            "type": "email",
            "value": "test@example.com",
        },
        "last_edited_by_property": {
            "key": "last_edited_by_property",
            "name": "Last edited by property",
            "type": "last_edited_by",
            "value": {
                "id": uuid.UUID("b66c20dd-0a48-4418-ae23-2d82ec151be3"),
                "name": "Michael Twomey",
                "type": "person",
                "avatar_url": "https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
                "email": "notion@mick.twomeylee.name",
                "is_bot": False,
            },
        },
        "number_property": {
            "key": "number_property",
            "name": "Number Property",
            "type": "number",
            "value": decimal.Decimal("5.23"),
        },
        "muti_select_property": {
            "key": "muti_select_property",
            "name": "Muti-select property",
            "type": "multi_select",
            "value": [
                {"name": "foo", "color": "gray"},
                {"name": "bar", "color": "brown"},
            ],
        },
        "relation_property": {
            "key": "relation_property",
            "name": "Relation Property",
            "type": "relation",
            "value": [uuid.UUID("ccad10e7-c776-423e-9662-6ad5fb1256d6")],
        },
        "number_rollup_property": {
            "key": "number_rollup_property",
            "name": "Number Rollup property",
            "type": "rollup",
            "value": decimal.Decimal("5.23"),
        },
        "file_property": {
            "key": "file_property",
            "name": "File property",
            "type": "files",
            "value": [{"name": "p8logo.png"}],
        },
        "date_property": {
            "key": "date_property",
            "name": "Date property",
            "type": "date",
            "value": {"start": datetime.date(2021, 7, 15), "end": None},
        },
        "date_rollup_property": {
            "key": "date_rollup_property",
            "name": "Date Rollup property",
            "type": "rollup",
            "value": {
                "start": datetime.datetime(
                    2021, 7, 15, 0, 0, tzinfo=datetime.timezone.utc
                ),
                "end": datetime.datetime(
                    2021, 7, 15, 0, 0, tzinfo=datetime.timezone.utc
                ),
            },
        },
        "created_by_property": {
            "key": "created_by_property",
            "name": "Created by property",
            "type": "created_by",
            "value": {
                "id": uuid.UUID("b66c20dd-0a48-4418-ae23-2d82ec151be3"),
                "name": "Michael Twomey",
                "type": "person",
                "avatar_url": "https://s3-us-west-2.amazonaws.com/public.notion-static.com/356f75b3-6f13-4f33-96c0-4c2be97ffe94/christmas_hk_mick_square.jpg",
                "email": "notion@mick.twomeylee.name",
                "is_bot": False,
            },
        },
        "text_property": {
            "key": "text_property",
            "name": "Text property",
            "type": "rich_text",
            "value": "Foo",
        },
        "created_time_property": {
            "key": "created_time_property",
            "name": "Created Time Property",
            "type": "created_time",
            "value": datetime.datetime(
                2021, 7, 31, 17, 1, tzinfo=datetime.timezone.utc
            ),
        },
        "string_formula_property": {
            "key": "string_formula_property",
            "name": "String Formula Property",
            "type": "formula",
            "value": "July 31 2021, 23:46",
        },
        "number_formula_property": {
            "key": "number_formula_property",
            "name": "Number Formula property",
            "type": "formula",
            "value": decimal.Decimal("6.23"),
        },
        "date_formula_property": {
            "key": "date_formula_property",
            "name": "Date Formula Property",
            "type": "formula",
            "value": {
                "start": datetime.datetime(
                    2021, 7, 31, 23, 46, tzinfo=datetime.timezone.utc
                ),
                "end": None,
            },
        },
        "email_rollup_property": {
            "key": "email_rollup_property",
            "name": "Email rollup property",
            "type": "rollup",
            "value": [{"type": "email", "email": "test@example.com"}],
        },
        "last_edited_time_property": {
            "key": "last_edited_time_property",
            "name": "Last Edited Time Property",
            "type": "last_edited_time",
            "value": datetime.datetime(
                2021, 7, 31, 18, 31, tzinfo=datetime.timezone.utc
            ),
        },
        "select_property": {
            "key": "select_property",
            "name": "Select property",
            "type": "select",
            "value": "gray",
        },
        "name": {
            "key": "name",
            "name": "Name",
            "type": "title",
            "value": "Fields filled in",
        },
    },
    "parent": uuid.UUID("fff51adc-8d4e-414a-a2e3-17e69111c328"),
    "parent_type": "database_id",
    "url": "https://www.notion.so/Fields-filled-in-ccad10e7c776423e96626ad5fb1256d6",
    "name": "Fields filled in",
    "type": "page",
}


def test_flatten_page():
    # Convert to dicts to make pytest diffs easier to read
    assert flatten_page(Page.parse_raw(EXAMPLE_PAGE_JSON)).dict() == EXAMPLE_FLAT_PAGE


EXAMPLE_FLAT_DATABASE = {
    "type": "database",
    "id": uuid.UUID("fff51adc-8d4e-414a-a2e3-17e69111c328"),
    "created_time": datetime.datetime(2021, 7, 31, 17, 1, tzinfo=datetime.timezone.utc),
    "last_edited_time": datetime.datetime(
        2021, 7, 31, 18, 20, tzinfo=datetime.timezone.utc
    ),
    "title": "API Test DB",
    "parent": True,
    "parent_type": "workspace",
    "properties": {
        "boolean_formula_property": {
            "key": "boolean_formula_property",
            "name": "Boolean Formula Property",
            "type": "formula",
            "value": "true",
        },
        "phone_property": {
            "key": "phone_property",
            "name": "Phone property",
            "type": "phone_number",
            "value": {},
        },
        "url_property": {
            "key": "url_property",
            "name": "URL property",
            "type": "url",
            "value": {},
        },
        "person_property": {
            "key": "person_property",
            "name": "Person property",
            "type": "people",
            "value": {},
        },
        "checkbox_property": {
            "key": "checkbox_property",
            "name": "Checkbox property",
            "type": "checkbox",
            "value": {},
        },
        "email_property": {
            "key": "email_property",
            "name": "Email property",
            "type": "email",
            "value": {},
        },
        "last_edited_by_property": {
            "key": "last_edited_by_property",
            "name": "Last edited by property",
            "type": "last_edited_by",
            "value": {},
        },
        "number_property": {
            "key": "number_property",
            "name": "Number Property",
            "type": "number",
            "value": "euro",
        },
        "muti_select_property": {
            "key": "muti_select_property",
            "name": "Muti-select property",
            "type": "multi_select",
            "value": ["gray", "brown"],
        },
        "relation_property": {
            "key": "relation_property",
            "name": "Relation Property",
            "type": "relation",
            "value": {
                "database_id": uuid.UUID("fff51adc-8d4e-414a-a2e3-17e69111c328"),
                "synced_property_name": "Relation Property",
                "synced_property_id": "_GWY",
            },
        },
        "number_rollup_property": {
            "key": "number_rollup_property",
            "name": "Number Rollup property",
            "type": "rollup",
            "value": {
                "relation_property_name": "Relation Property",
                "relation_property_id": "_GWY",
                "rollup_property_name": "Number Property",
                "rollup_property_id": "S>XJ",
                "function": "sum",
            },
        },
        "file_property": {
            "key": "file_property",
            "name": "File property",
            "type": "files",
            "value": {},
        },
        "date_property": {
            "key": "date_property",
            "name": "Date property",
            "type": "date",
            "value": {},
        },
        "date_rollup_property": {
            "key": "date_rollup_property",
            "name": "Date Rollup property",
            "type": "rollup",
            "value": {
                "relation_property_name": "Relation Property",
                "relation_property_id": "_GWY",
                "rollup_property_name": "Date property",
                "rollup_property_id": "eo~[",
                "function": "date_range",
            },
        },
        "created_by_property": {
            "key": "created_by_property",
            "name": "Created by property",
            "type": "created_by",
            "value": {},
        },
        "text_property": {
            "key": "text_property",
            "name": "Text property",
            "type": "rich_text",
            "value": {},
        },
        "created_time_property": {
            "key": "created_time_property",
            "name": "Created Time Property",
            "type": "created_time",
            "value": {},
        },
        "string_formula_property": {
            "key": "string_formula_property",
            "name": "String Formula Property",
            "type": "formula",
            "value": 'formatDate(now(), "MMMM D YYYY, HH:mm")',
        },
        "number_formula_property": {
            "key": "number_formula_property",
            "name": "Number Formula property",
            "type": "formula",
            "value": 'prop("Number Property") + 1',
        },
        "date_formula_property": {
            "key": "date_formula_property",
            "name": "Date Formula Property",
            "type": "formula",
            "value": "now()",
        },
        "email_rollup_property": {
            "key": "email_rollup_property",
            "name": "Email rollup property",
            "type": "rollup",
            "value": {
                "relation_property_name": "Relation Property",
                "relation_property_id": "_GWY",
                "rollup_property_name": "Email property",
                "rollup_property_id": "Mqx<",
                "function": "show_original",
            },
        },
        "last_edited_time_property": {
            "key": "last_edited_time_property",
            "name": "Last Edited Time Property",
            "type": "last_edited_time",
            "value": {},
        },
        "select_property": {
            "key": "select_property",
            "name": "Select property",
            "type": "select",
            "value": ["gray"],
        },
        "name": {"key": "name", "name": "Name", "type": "title", "value": {}},
    },
}


def test_flatten_database():
    # Convert to dicts to make pytest diffs easier to read
    assert (
        flatten_database(Database.parse_raw(EXAMPLE_DATABASE_JSON)).dict()
        == EXAMPLE_FLAT_DATABASE
    )


def test_flatten_item():
    assert (
        flatten_item(Database.parse_raw(EXAMPLE_DATABASE_JSON)).dict()
        == EXAMPLE_FLAT_DATABASE
    )
    assert flatten_item(Page.parse_raw(EXAMPLE_PAGE_JSON)).dict() == EXAMPLE_FLAT_PAGE
