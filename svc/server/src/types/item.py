from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic import Field as PydanticField
from pydantic import (
    SerializationInfo,
    ValidationInfo,
    field_serializer,
    field_validator,
)
from src.types.type import FieldAcceptableType, FieldType


class TableItemField(BaseModel):
    """Model represents field in the item."""

    field_type: FieldType
    field_name: str
    field_value: FieldAcceptableType | None

    @field_validator("field_value", mode="before")
    @classmethod
    def validate_field_value(
        cls, value: Any, _info: ValidationInfo
    ) -> FieldAcceptableType:
        """Validate value passed to the field.

        Parameters
        ----------
        value : Any
            Value to be validated.
        _info : ValidationInfo
            Context info containing data.

        Returns
        -------
        FieldAcceptableType
            Properly validated value.
        """
        field_type: FieldType = _info.data["field_type"]

        if isinstance(value, datetime):
            return value

        return field_type.validate(value)

    @field_serializer("field_value")
    def _serialize_field_value(
        self, value: FieldAcceptableType, _info: SerializationInfo
    ) -> int | float | str:
        if isinstance(value, datetime):
            return value.isoformat()
        return value


class TableItem(BaseModel):
    """Model represents item (row) in the table."""

    id: str | None = PydanticField(None, alias="_id")
    items: list[TableItemField]

    @field_validator("id", mode="before")
    @classmethod
    def _validate_id(cls, value: Any) -> str:
        return str(value)
