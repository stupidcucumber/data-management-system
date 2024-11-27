from pydantic import BaseModel
from pymongo.collection import ObjectId


class DatabaseName(BaseModel):
    """Model represents name of the database."""

    database_name: str


class Database(BaseModel):
    """Model represents Database entity in the DMS."""

    _id: ObjectId | None
    database_name: str
    table_names: list[str]
