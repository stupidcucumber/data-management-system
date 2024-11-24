from datetime import datetime
from enum import StrEnum
from typing import Any

from dateutil.parser import parse
from src.types.dateinvl import DateInterval

FieldAcceptableType = int | str | float | datetime | DateInterval


class FieldType(StrEnum):
    """Available field types in the DMS."""

    INTEGER: str = "integer"
    REAL: str = "real"
    CHAR: str = "char"
    STRING: str = "string"
    DATE: str = "date"
    DATE_INTERVAL: str = "dateInvl"

    def _validate_integer(self, value: Any) -> int:
        if not isinstance(value, int):
            raise ValueError("bad values provided to the field.")
        return value

    def _validate_real(self, value: Any) -> float:
        if not isinstance(value, float):
            raise ValueError("bad values provided to the field.")
        return value

    def _validate_char(self, value: Any) -> str:
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError("bad values provided to the field.")
        return value

    def _validate_string(self, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError("bad values provided to the field.")
        return value

    def _validate_date(self, value: Any) -> datetime:
        result = parse(value)
        return result

    def _validate_date_interval(self, value: Any) -> DateInterval:
        result = DateInterval(**value)
        return result

    def validate(self, value: Any) -> FieldAcceptableType:
        """Check whether the provided value is valid.

        Parameters
        ----------
        value : Any
            Value that needs to be checked against its type.

        Returns
        -------
        FieldAcceptableType
            True if valid is checks in with its type.
        """
        return self.__getattribute__("_validate_" + self._name_.lower())(value)
