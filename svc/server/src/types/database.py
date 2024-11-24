from pydantic import BaseModel
from pymongo.collection import ObjectId


class Database(BaseModel):
    """Model represents Database entity in the DMS."""

    _id: ObjectId | None
    database_name: str
    table_names: list[str]
