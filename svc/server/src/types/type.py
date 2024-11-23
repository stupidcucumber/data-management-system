from enum import StrEnum
from typing import Any, Callable

from dateutil.parser import ParserError, parse
from pydantic import ValidationError
from src.types.dateinvl import DateInterval


class FieldType(StrEnum):
    """Available field types in the DMS."""

    INTEGER: str = "integer"
    REAL: str = "real"
    CHAR: str = "char"
    STRING: str = "string"
    DATE: str = "date"
    DATE_INTERVAL: str = "dateInvl"

    def _validate_integer(self, value: Any) -> bool:
        return isinstance(value, int)

    def _validate_real(self, value: Any) -> bool:
        return isinstance(value, float)

    def _validate_char(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        return len(value) == 1

    def _validate_string(self, value: Any) -> bool:
        return isinstance(value, str)

    def _validate_date(self, value: Any) -> bool:
        is_valid = True
        try:
            parse(value)
        except ParserError:
            is_valid = False
        return is_valid

    def _validate_date_interval(self, value: Any) -> bool:
        is_valid = True
        try:
            DateInterval(**value)
        except ValidationError:
            is_valid = False
        return is_valid

    @property
    def validators(self) -> dict[str, Callable[[Any], bool]]:
        """All validator methods.

        Returns
        -------
        dict[str, Callable[[Any], bool]]
            Dictionary of all validators and their functions.
        """
        return {
            key: value
            for key, value in self.__dict__.items()
            if key.startswith("_validate")
        }

    def validate(self, value: Any) -> bool:
        """Check whether the provided value is valid.

        Parameters
        ----------
        value : Any
            Value that needs to be checked against its type.

        Returns
        -------
        bool
            True if valid is checks in with its type.
        """
        return self.validators["_validate" + self._name_.lower()](value)
