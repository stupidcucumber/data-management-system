from typing import Any

from pydantic import BaseModel
from pydantic import Field as PydanticField
from pydantic import ValidationInfo, field_validator
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
        return field_type.validate(value)


class TableItem(BaseModel):
    """Model represents item (row) in the table."""

    id: str | None = PydanticField(None, alias="_id")
    items: list[TableItemField]
