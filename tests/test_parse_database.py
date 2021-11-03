import json

from notions.models.database import Database

# notions api GET /v1/databases/fff51adc-8d4e-414a-a2e3-17e69111c328 | jq . | pbcopy
# Modified 00.000Z -> 00+00:00 to make roundtrip comparison easier
# Fixed up \" -> \\" to make parsing work
EXAMPLE_DATABASE_JSON = """
{
  "object": "database",
  "id": "fff51adc-8d4e-414a-a2e3-17e69111c328",
  "created_time": "2021-07-31T17:01:00+00:00",
  "last_edited_time": "2021-07-31T18:20:00+00:00",
  "title": [
    {
      "type": "text",
      "text": {
        "content": "API Test DB",
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
      "plain_text": "API Test DB",
      "href": null
    }
  ],
  "properties": {
    "Boolean Formula Property": {
      "id": "::TX",
      "name": "Boolean Formula Property",
      "type": "formula",
      "formula": {
        "expression": "true"
      }
    },
    "Phone property": {
      "id": ":Cyi",
      "name": "Phone property",
      "type": "phone_number",
      "phone_number": {}
    },
    "URL property": {
      "id": ">KRE",
      "name": "URL property",
      "type": "url",
      "url": {}
    },
    "Person property": {
      "id": "EZD;",
      "name": "Person property",
      "type": "people",
      "people": {}
    },
    "Checkbox property": {
      "id": "L%3C%7D%40",
      "name": "Checkbox property",
      "type": "checkbox",
      "checkbox": {}
    },
    "Email property": {
      "id": "Mqx%3C",
      "name": "Email property",
      "type": "email",
      "email": {}
    },
    "Last edited by property": {
      "id": "Q>n|",
      "name": "Last edited by property",
      "type": "last_edited_by",
      "last_edited_by": {}
    },
    "Number Property": {
      "id": "S>XJ",
      "name": "Number Property",
      "type": "number",
      "number": {
        "format": "euro"
      }
    },
    "Muti-select property": {
      "id": "TrTf",
      "name": "Muti-select property",
      "type": "multi_select",
      "multi_select": {
        "options": [
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
      }
    },
    "Relation Property": {
      "id": "_GWY",
      "name": "Relation Property",
      "type": "relation",
      "relation": {
        "database_id": "fff51adc-8d4e-414a-a2e3-17e69111c328",
        "synced_property_name": "Relation Property",
        "synced_property_id": "_GWY"
      }
    },
    "Number Rollup property": {
      "id": "`<GE",
      "name": "Number Rollup property",
      "type": "rollup",
      "rollup": {
        "rollup_property_name": "Number Property",
        "relation_property_name": "Relation Property",
        "rollup_property_id": "S>XJ",
        "relation_property_id": "_GWY",
        "function": "sum"
      }
    },
    "File property": {
      "id": "dVLG",
      "name": "File property",
      "type": "files",
      "files": {}
    },
    "Date property": {
      "id": "eo~%5B",
      "name": "Date property",
      "type": "date",
      "date": {}
    },
    "Date Rollup property": {
      "id": "fm%5Dd",
      "name": "Date Rollup property",
      "type": "rollup",
      "rollup": {
        "rollup_property_name": "Date property",
        "relation_property_name": "Relation Property",
        "rollup_property_id": "eo~%5B",
        "relation_property_id": "_GWY",
        "function": "date_range"
      }
    },
    "Created by property": {
      "id": "f%7Bol",
      "name": "Created by property",
      "type": "created_by",
      "created_by": {}
    },
    "Text property": {
      "id": "keEA",
      "name": "Text property",
      "type": "rich_text",
      "rich_text": {}
    },
    "Created Time Property": {
      "id": "l%3BMe",
      "name": "Created Time Property",
      "type": "created_time",
      "created_time": {}
    },
    "String Formula Property": {
      "id": "n`}C",
      "name": "String Formula Property",
      "type": "formula",
      "formula": {
        "expression": "formatDate(now(), \\"MMMM D YYYY, HH:mm\\")"
      }
    },
    "Number Formula property": {
      "id": "oNn>",
      "name": "Number Formula property",
      "type": "formula",
      "formula": {
        "expression": "prop(\\"Number Property\\") + 1"
      }
    },
    "Date Formula Property": {
      "id": "oyUS",
      "name": "Date Formula Property",
      "type": "formula",
      "formula": {
        "expression": "now()"
      }
    },
    "Email rollup property": {
      "id": "viJS",
      "name": "Email rollup property",
      "type": "rollup",
      "rollup": {
        "rollup_property_name": "Email property",
        "relation_property_name": "Relation Property",
        "rollup_property_id": "Mqx%3C",
        "relation_property_id": "_GWY",
        "function": "show_original"
      }
    },
    "Last Edited Time Property": {
      "id": "yoI=",
      "name": "Last Edited Time Property",
      "type": "last_edited_time",
      "last_edited_time": {}
    },
    "Select property": {
      "id": "}XVI",
      "name": "Select property",
      "type": "select",
      "select": {
        "options": [
          {
            "id": "6492d7c0-0245-4052-b410-aecc6f882ead",
            "name": "foo",
            "color": "gray"
          }
        ]
      }
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


def test_parse_database_roundtrip():
    assert json.loads(Database.parse_raw(EXAMPLE_DATABASE_JSON).json()) == json.loads(
        EXAMPLE_DATABASE_JSON
    )
