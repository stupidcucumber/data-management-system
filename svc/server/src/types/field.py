from typing import Any

from pydantic import BaseModel, ValidationInfo, field_validator
from src.types.type import FieldAcceptableType, FieldType


class Field(BaseModel):
    """Model that represents field in the table."""

    field_type: FieldType
    field_name: str
    field_value: FieldAcceptableType

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
