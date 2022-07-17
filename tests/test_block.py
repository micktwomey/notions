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

GENERIC_COLOR = color.Color.default

GENERIC_RICH_TEXT = [
    {
        "type": "text",
        "plain_text": "Lacinato kale",
        "text": {"content": "Lacinato kale"},
    }
]

GENERIC_CHILDREN = [
    {
        **GENERIC_BLOCK,
        **{
            "type": "heading_1",
            "heading_1": {"rich_text": GENERIC_RICH_TEXT, "color": GENERIC_COLOR},
        },
    }
]

GENERIC_EMOJI = {"type": "emoji", "emoji": "🤪"}

GENERIC_FILE = {
    "name": "myfile.jpg",
    "type": "external",
    "external": {"url": "https://example.com/myfile.jpg"},
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
                    "rich_text": GENERIC_RICH_TEXT,
                    "color": GENERIC_COLOR,
                },
            },
            block.Heading1Block,
        ),
        (
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": GENERIC_RICH_TEXT,
                    "color": GENERIC_COLOR,
                },
            },
            block.Heading2Block,
        ),
        (
            {
                "type": "heading_3",
                "heading_3": {
                    "rich_text": GENERIC_RICH_TEXT,
                    "color": GENERIC_COLOR,
                },
            },
            block.Heading3Block,
        ),
        (
            {
                "type": "callout",
                "callout": {
                    "rich_text": GENERIC_RICH_TEXT,
                    "icon": GENERIC_EMOJI,
                    "color": GENERIC_COLOR,
                    "children": GENERIC_CHILDREN,
                },
            },
            block.CalloutBlock,
        ),
        (
            {
                "type": "quote",
                "quote": {
                    "rich_text": GENERIC_RICH_TEXT,
                    "color": GENERIC_COLOR,
                    "children": GENERIC_CHILDREN,
                },
            },
            block.QuoteBlock,
        ),
        (
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "color": GENERIC_COLOR,
                    "children": GENERIC_CHILDREN,
                },
            },
            block.BulletedListItemBlock,
        ),
        (
            {
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "color": GENERIC_COLOR,
                    "children": GENERIC_CHILDREN,
                },
            },
            block.NumberedListItemBlock,
        ),
        (
            {
                "type": "to_do",
                "to_do": {
                    "rich_text": GENERIC_RICH_TEXT,
                    "checked": True,
                    "color": GENERIC_COLOR,
                    "children": GENERIC_CHILDREN,
                },
            },
            block.TodoBlock,
        ),
        (
            {
                "type": "toggle",
                "toggle": {
                    "rich_text": GENERIC_RICH_TEXT,
                    "color": GENERIC_COLOR,
                    "children": GENERIC_CHILDREN,
                },
            },
            block.ToggleBlock,
        ),
        (
            {
                "type": "code",
                "code": {
                    "rich_text": GENERIC_RICH_TEXT,
                    "caption": GENERIC_RICH_TEXT,
                    "language": block.Language.python,
                },
            },
            block.CodeBlock,
        ),
        (
            {
                "type": "child_page",
                "child_page": {
                    "title": "Child Page",
                },
            },
            block.ChildPageBlock,
        ),
        (
            {
                "type": "child_database",
                "child_database": {
                    "title": "Child Page",
                },
            },
            block.ChildDatabaseBlock,
        ),
        (
            {
                "type": "embed",
                "embed": {
                    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                },
            },
            block.EmbedBlock,
        ),
        (
            {
                "type": "image",
                "image": {
                    "image": GENERIC_FILE,
                },
            },
            block.ImageBlock,
        ),
        (
            {
                "type": "video",
                "video": {
                    "video": GENERIC_FILE,
                },
            },
            block.VideoBlock,
        ),
        (
            {
                "type": "file",
                "file": {
                    "file": GENERIC_FILE,
                    "caption": GENERIC_RICH_TEXT,
                },
            },
            block.FileBlock,
        ),
        (
            {
                "type": "pdf",
                "pdf": {
                    "pdf": GENERIC_FILE,
                },
            },
            block.PdfBlock,
        ),
        (
            {
                "type": "bookmark",
                "bookmark": {
                    "url": "https://example.com/",
                    "caption": GENERIC_RICH_TEXT,
                },
            },
            block.BookmarkBlock,
        ),
        (
            {
                "type": "equation",
                "equation": {
                    "expression": "x = 1 / y",
                },
            },
            block.EquationBlock,
        ),
        (
            {
                "type": "divider",
            },
            block.DividerBlock,
        ),
        (
            {
                "type": "table_of_contents",
                "table_of_contents": {
                    "color": GENERIC_COLOR,
                },
            },
            block.TableOfContentsBlock,
        ),
        (
            {
                "type": "breadcrumb",
            },
            block.BreadcrumbBlock,
        ),
        (
            {
                "type": "column",
                "column": {"children": GENERIC_CHILDREN},
            },
            block.ColumnBlock,
        ),
        (
            {
                "type": "column_list",
                "column_list": {
                    "children": [
                        {
                            **GENERIC_BLOCK,
                            **{
                                "type": "column",
                                "column": {"children": GENERIC_CHILDREN},
                            },
                        }
                    ]
                },
            },
            block.ColumnListBlock,
        ),
        (
            {
                "type": "link_preview",
                "link_preview": {"url": "https://example.com/"},
            },
            block.LinkPreviewBlock,
        ),
        (
            {
                "type": "template",
                "template": {
                    "rich_text": GENERIC_RICH_TEXT,
                    "children": GENERIC_CHILDREN,
                },
            },
            block.TemplateBlock,
        ),
        (
            {
                "type": "link_to_page",
                "link_to_page": {
                    "type": "database_id",
                    "database_id": uuid.UUID("18ba39c7-b2ef-41d0-8133-e8f8b1723700"),
                },
            },
            block.LinkToPageBlock,
        ),
    ],
)
def test_roundtrip(json_block: dict, block_type: block.Block):
    expected = {**GENERIC_BLOCK, **json_block}
    parsed = block_type.parse_obj(expected)
    assert expected == parsed.dict(exclude_none=True, exclude_unset=True)
