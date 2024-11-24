from pydantic import BaseModel
from pydantic import Field as PydanticField
from pydantic import (
    SerializationInfo,
    ValidationInfo,
    field_serializer,
    field_validator,
)
from pymongo.collection import ObjectId
from src.types.field import Field


class Table(BaseModel):
    """Model representing Table entity in the DMS."""

    id: str | None = PydanticField(None, alias="_id")
    database_name: str
    table_name: str
    table_fields: list[Field]

    @field_validator("id", mode="before")
    @classmethod
    def _validate_id(cls, value: ObjectId | None, _info: ValidationInfo) -> str | None:
        if not value:
            return None
        return str(value)

    @field_serializer("id")
    def _serialize_id(
        self, _id: ObjectId | None, _info: SerializationInfo
    ) -> str | None:
        if not _id:
            return None
        return str(_id)

    @property
    def columns(self) -> set[str]:
        """Field names.

        Returns
        -------
        set[str]
            A set of names of all fields in the table.
        """
        return [field.field_name for field in self.table_fields]

    def field(self, name: str) -> Field | None:
        """Extract field with a specific name.

        Parameters
        ----------
        name : str
            Name of the desired field to search for.

        Returns
        -------
        Field | None
            If there is a field with this name returns it,
            otherwise returns None.
        """
        for field in self.table_fields:
            if field.field_name == name:
                return field
        return None
