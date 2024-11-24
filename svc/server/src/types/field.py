from pydantic import BaseModel
from src.types.type import FieldType


class Field(BaseModel):
    """Model that represents field in the table."""

    field_type: FieldType
    field_name: str
