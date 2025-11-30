"""Schemas for routine operations."""

from pydantic import BaseModel, field_validator

from src.routing.routine.utils import RoutineUtils


class Routine(BaseModel):
    """Schema for routine request."""

    routine_id: int
    start_time: str
    end_time: str
    weekday: int

    @field_validator("weekday", mode="before")
    def validate_weekday(cls, value: int) -> int:
        """Validate that the weekday is between 0 and 6."""
        return RoutineUtils.validate_weekday(value)

    @field_validator("start_time", "end_time", mode="before")
    def validate_time(cls, value: str) -> str:
        """Validate that the weekday is one of the allowed values."""
        return RoutineUtils.validate_time(value)
