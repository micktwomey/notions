import uuid

import iso8601
import pytest

from notions.models import block, color

# Examples in the docs tend to omit this preamble
GENERIC_BLOCK = {
    "object": "block",
    "id": uuid.UUID("9bc30ad4-9373-46a5-84ab-0a7845ee52e6"),
    "created_time": iso8601.parse_date("2021-03-16T16:31:00.000Z"),
    "created_by": {"object": "user", "id": "cb38e95d-00cf-4e7e-adce-974f4a44a547"},
    "last_edited_time": iso8601.parse_date("2021-03-16T16:32:00.000Z"),
    "last_edited_by": {
        "object": "user",
        "id": uuid.UUID("e79a0b74-3aba-4149-9f74-0bb5791a6ee6"),
    },
    "has_children": False,
    "archived": False,
}


@pytest.mark.parametrize(
    "json_block,block_type",
    [
        (
            {
                "type": "link_to_page",
                "link_to_page": {
                    "type": "page_id",
                    "page_id": uuid.UUID("bfaa7747-ba2b-4870-bc48-3f4777e579b5"),
                },
            },
            block.LinkToPageBlock,
        ),
        (
            {
                "type": "link_to_page",
                "link_to_page": {
                    "type": "database_id",
                    "database_id": uuid.UUID("bfaa7747-ba2b-4870-bc48-3f4777e579b5"),
                },
            },
            block.LinkToPageBlock,
        ),
        (
            {
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "plain_text": "Lacinato kale",
                            "text": {"content": "Lacinato kale"},
                        }
                    ],
                    "color": color.Color.default,
                },
            },
            block.Heading1Block,
        ),
        (
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "plain_text": "Lacinato kale",
                            "text": {"content": "Lacinato kale"},
                        }
                    ],
                    "color": color.Color.default,
                },
            },
            block.Heading2Block,
        ),
        (
            {
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "plain_text": "Lacinato kale",
                            "text": {"content": "Lacinato kale"},
                        }
                    ],
                    "color": color.Color.default,
                },
            },
            block.Heading3Block,
        ),
        (
            {
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {
                            "type": "text",
                            "plain_text": "Lacinato kale",
                            "text": {"content": "Lacinato kale"},
                        }
                    ],
                    "icon": {"type": "emoji", "emoji": "🤪"},
                    "color": color.Color.default,
                    "children": [],
                },
            },
            block.CalloutBlock,
        ),
    ],
)
def test_roundtrip(json_block: dict, block_type: block.Block):
    expected = {**GENERIC_BLOCK, **json_block}
    parsed = block_type.parse_obj(expected)
    assert expected == parsed.dict(exclude_none=True, exclude_unset=True)
