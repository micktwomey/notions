"""Properties of pages and databases

Split into request properties used for creation and content properties
"""

import typing

from .checkbox import DatabaseCheckboxProperty, PageCheckboxProperty
from .created_by import DatabaseCreatedByProperty, PageCreatedByProperty
from .created_time import (
    CreatePageCreatedTimeProperty,
    DatabaseCreatedTimeProperty,
    PageCreatedTimeProperty,
)
from .date import DatabaseDateProperty, PageDateProperty
from .email import DatabaseEmailProperty, PageEmailProperty
from .file import DatabaseFileProperty, PageFileProperty
from .formula import DatabaseFormulaProperty, PageFormulaProperty
from .last_edited_by import DatabaseLastEditedByProperty, PageLastEditedByProperty
from .last_edited_time import DatabaseLastEditedTimeProperty, PageLastEditedTimeProperty
from .multi_select import DatabaseMultiSelectProperty, PageMultiSelectProperty
from .number import (
    CreateDatabaseNumberProperty,
    CreatePageNumberProperty,
    DatabaseNumberProperty,
    PageNumberProperty,
)
from .people import DatabasePeopleProperty, PagePeopleProperty
from .phone_number import DatabasePhoneNumberProperty, PagePhoneNumberProperty
from .relation import DatabaseRelationProperty, PageRelationProperty
from .rich_text import DatabaseRichTextProperty, PageRichTextProperty
from .rollup import DatabaseRollupProperty, PageRollupProperty
from .select import CreatePageSelectProperty, DatabaseSelectProperty, PageSelectProperty
from .title import (
    CreateDatabaseTitleProperty,
    CreatePageTitleProperty,
    DatabaseTitleProperty,
    PageTitleProperty,
)
from .url import CreatePageURLProperty, DatabaseURLProperty, PageURLProperty

DatabaseProperty = typing.Union[
    DatabaseCheckboxProperty,
    DatabaseCreatedByProperty,
    DatabaseCreatedTimeProperty,
    DatabaseDateProperty,
    DatabaseEmailProperty,
    DatabaseFileProperty,
    DatabaseFormulaProperty,
    DatabaseLastEditedByProperty,
    DatabaseLastEditedTimeProperty,
    DatabaseMultiSelectProperty,
    DatabaseNumberProperty,
    DatabasePeopleProperty,
    DatabasePhoneNumberProperty,
    DatabaseRelationProperty,
    DatabaseRichTextProperty,
    DatabaseRollupProperty,
    DatabaseSelectProperty,
    DatabaseTitleProperty,
    DatabaseURLProperty,
]

DatabaseProperties = typing.Dict[str, DatabaseProperty]

CreateDatabaseProperty = typing.Union[
    CreateDatabaseNumberProperty,
    # TODO: CreateDatabaseSelectProperty,
    # TODO: CreateDatabaseCreatedTimeProperty,
    # TODO: CreateDatabaseURLProperty,
    CreateDatabaseTitleProperty,
    # TODO: CreateDatabaseRichTextProperty,
    # TODO: CreateDatabaseDateProperty,
    # TODO: CreateDatabaseFileProperty,
    # TODO: CreateDatabasePeopleProperty,
    # TODO: CreateDatabaseCheckboxProperty,
    # TODO: CreateDatabaseEmailProperty,
    # TODO: CreateDatabasePhoneNumberProperty,
    # TODO: CreateDatabaseMultiSelectProperty,
    # TODO: CreateDatabaseFormulaProperty,
    # TODO: CreateDatabaseRollupProperty,
    # TODO: CreateDatabaseCreatedByProperty,
    # TODO: CreateDatabaseLastEditedTimeProperty,
    # TODO: CreateDatabaseLastEditedByProperty,
    # TODO: CreateDatabaseRelationProperty,
]

CreateDatabaseProperties = typing.Dict[str, CreateDatabaseProperty]

PageProperty = typing.Union[
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
]

PageProperties = typing.Dict[str, PageProperty]

CreatePageProperty = typing.Union[
    CreatePageNumberProperty,
    CreatePageSelectProperty,
    CreatePageCreatedTimeProperty,
    CreatePageURLProperty,
    CreatePageTitleProperty,
    # TODO: CreatePageRichTextProperty,
    # TODO: CreatePageDateProperty,
    # TODO: CreatePageFileProperty,
    # TODO: CreatePagePeopleProperty,
    # TODO: CreatePageCheckboxProperty,
    # TODO: CreatePageEmailProperty,
    # TODO: CreatePagePhoneNumberProperty,
    # TODO: CreatePageMultiSelectProperty,
    # TODO: CreatePageFormulaProperty,
    # TODO: CreatePageRollupProperty,
    # TODO: CreatePageCreatedByProperty,
    # TODO: CreatePageLastEditedTimeProperty,
    # TODO: CreatePageLastEditedByProperty,
    # TODO: CreatePageRelationProperty,
]

CreatePageProperties = typing.Dict[str, CreatePageProperty]

__all__ = [
    "DatabaseProperty",
    "DatabaseProperties",
    "DatabaseCheckboxProperty",
    "DatabaseCreatedByProperty",
    "DatabaseCreatedTimeProperty",
    "DatabaseDateProperty",
    "DatabaseEmailProperty",
    "DatabaseFileProperty",
    "DatabaseFormulaProperty",
    "DatabaseLastEditedByProperty",
    "DatabaseLastEditedTimeProperty",
    "DatabaseMultiSelectProperty",
    "DatabaseNumberProperty",
    "DatabasePeopleProperty",
    "DatabasePhoneNumberProperty",
    "DatabaseRelationProperty",
    "DatabaseRichTextProperty",
    "DatabaseRollupProperty",
    "DatabaseSelectProperty",
    "DatabaseTitleProperty",
    "DatabaseURLProperty",
    "CreateDatabaseProperty",
    "CreateDatabaseProperties",
    "CreateDatabaseNumberProperty",
    # TODO: CreateDatabaseSelectProperty,
    # TODO: CreateDatabaseCreatedTimeProperty,
    # TODO: CreateDatabaseURLProperty,
    "CreateDatabaseTitleProperty",
    # TODO: CreateDatabaseRichTextProperty,
    # TODO: CreateDatabaseDateProperty,
    # TODO: CreateDatabaseFileProperty,
    # TODO: CreateDatabasePeopleProperty,
    # TODO: CreateDatabaseCheckboxProperty,
    # TODO: CreateDatabaseEmailProperty,
    # TODO: CreateDatabasePhoneNumberProperty,
    # TODO: CreateDatabaseMultiSelectProperty,
    # TODO: CreateDatabaseFormulaProperty,
    # TODO: CreateDatabaseRollupProperty,
    # TODO: CreateDatabaseCreatedByProperty,
    # TODO: CreateDatabaseLastEditedTimeProperty,
    # TODO: CreateDatabaseLastEditedByProperty,
    # TODO: CreateDatabaseRelationProperty,
    "PageProperty",
    "PageProperties",
    "PageCheckboxProperty",
    "PageCreatedByProperty",
    "PageCreatedTimeProperty",
    "PageDateProperty",
    "PageEmailProperty",
    "PageFileProperty",
    "PageFormulaProperty",
    "PageLastEditedByProperty",
    "PageLastEditedTimeProperty",
    "PageMultiSelectProperty",
    "PageNumberProperty",
    "PagePeopleProperty",
    "PagePhoneNumberProperty",
    "PageRelationProperty",
    "PageRichTextProperty",
    "PageRollupProperty",
    "PageSelectProperty",
    "PageTitleProperty",
    "PageURLProperty",
    "CreatePageProperty",
    "CreatePageProperties",
    "CreatePageNumberProperty",
    "CreatePageSelectProperty",
    "CreatePageCreatedTimeProperty",
    "CreatePageURLProperty",
    "CreatePageTitleProperty",
    # TODO: CreatePageRichTextProperty,
    # TODO: CreatePageDateProperty,
    # TODO: CreatePageFileProperty,
    # TODO: CreatePagePeopleProperty,
    # TODO: CreatePageCheckboxProperty,
    # TODO: CreatePageEmailProperty,
    # TODO: CreatePagePhoneNumberProperty,
    # TODO: CreatePageMultiSelectProperty,
    # TODO: CreatePageFormulaProperty,
    # TODO: CreatePageRollupProperty,
    # TODO: CreatePageCreatedByProperty,
    # TODO: CreatePageLastEditedTimeProperty,
    # TODO: CreatePageLastEditedByProperty,
    # TODO: CreatePageRelationProperty,
]
