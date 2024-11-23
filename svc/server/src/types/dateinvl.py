from datetime import datetime

from dateutil.parser import parse
from pydantic import (
    BaseModel,
    SerializationInfo,
    ValidationError,
    ValidationInfo,
    field_serializer,
    field_validator,
)


class DateInterval(BaseModel):
    """Type representing date interval."""

    start_date: datetime | str
    end_date: datetime | str

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def validate_dateteime_objects(
        cls, date: datetime | str, _info: ValidationInfo
    ) -> datetime:
        """Validate passed parameter.

        Parameters
        ----------
        date : datetime | str
            Object to be parsed.
        _info : ValidationInfo
            Additional info that may help to properly
            validate object.

        Returns
        -------
        datetime
            Properly validates date object.

        Raises
        ------
        ValidationError
            If date passed into the object constructor does not match
            any of the date formats.
        """
        if isinstance(date, datetime):
            return date

        try:
            result = parse(date)
        except ValueError:
            raise ValidationError(f"{date} is not matching any formats of date!")

        return result

    @field_serializer("start_date", "end_date")
    @classmethod
    def serialize_datetime_objects(
        self, date: datetime, _info: SerializationInfo
    ) -> str:
        """Serialize datetime objects..

        Parameters
        ----------
        date : datetime
            Object to be serialized.
        _info : SerializationInfo
            Additional info that may help to properly
            serialize object.

        Returns
        -------
        str
            Properly serialized date object into
            ISO format.
        """
        return date.isoformat()
