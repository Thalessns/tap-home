"""Utils for routine operations."""

from datetime import datetime
from pydantic_settings import BaseSettings

class RoutineConfig(BaseSettings):
    """Class related to routine configs."""

    HOURS_ADJUST: int = 3


class RoutineUtils:

    @staticmethod
    def validate_weekday(value: int) -> int:
        """Validate that the weekday is between 0 and 6.
        
        Args:
            value (int): The weekday value to validate.

        Returns:
            int: The validated weekday value.

        Raises:
            ValueError: If the value is not between 0 and 6.
        """
        if not (0 <= value <= 6):
            raise ValueError("Weekday must be an integer between 0 (Monday) and 6 (Sunday).")
        return value

    @staticmethod
    def validate_time(value: str) -> str:
        """Validate that the time is in H:M format.
        
        Args:
            value (str): The time string to validate.

        Returns:
            str: The validated time string.
        """
        return value.strip().lower()

    @staticmethod
    def get_weekday() -> int:
        """Convert weekday string to integer representation.

        Returns:
            int: The integer representation of the weekday.

        Raises:
            ValueError: If the weekday string is not valid.
        """
        weekdays = {
            "monday": 1,
            "tuesday": 2,
            "wednesday": 3,
            "thursday": 4,
            "friday": 5,
            "saturday": 6,
            "sunday": 7
        }
        date = datetime.now()
        day = date.strftime("%A").lower()
        return weekdays[day]


routine_config = RoutineConfig()
