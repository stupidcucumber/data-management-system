from pydantic import BaseModel
from pymongo.collection import ObjectId
from src.types.field import Field


class Table(BaseModel):
    """Model representing Table entity in the DMS."""

    _id: ObjectId | None
    database_name: str
    table_name: str
    table_fields: list[Field]

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
