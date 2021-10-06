import typing
import uuid

import pydantic


class DatabaseRelation(pydantic.BaseModel):
    database_id: uuid.UUID
    synced_property_name: typing.Optional[str]
    synced_property_id: typing.Optional[str]

    def get_value(self):
        return {
            "database_id": self.database_id,
            "synced_property_name": self.synced_property_name,
            "synced_property_id": self.synced_property_id,
        }


class DatabaseRelationProperty(pydantic.BaseModel):
    id: str
    name: str
    type: typing.Literal["relation"] = "relation"
    relation: DatabaseRelation

    def get_value(self):
        return self.relation.get_value()


class PageRelation(pydantic.BaseModel):
    id: uuid.UUID

    def get_value(self):
        return self.id


class PageRelationProperty(pydantic.BaseModel):
    id: str
    type: typing.Literal["relation"] = "relation"
    relation: typing.List[PageRelation]

    def get_value(self):
        return [relation.get_value() for relation in self.relation]
