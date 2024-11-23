from typing import Any

from pydantic import BaseModel
from src.types.field import Field


class Table(BaseModel):
    """Model representing Table entity in the DMS."""

    database: str
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

    def _validate_entry(self, entry: dict[str, Any]) -> bool:
        """Validate input entry.

        Checks the validity of the entry by:
        - First, comparing sets of keys.
        - Second, checking types of the values provided against
        types of the corresponding fields in the table.

        Parameters
        ----------
        entry : dict[str, Any]
            Entry that is to be inserted into the table.

        Returns
        -------
        bool
            True if entry can be inserted into the table.
        """
        if set(entry.keys()) != self.columns:
            return False

        return all((self.field(key).field_type.validate(value) for key, value in entry))
