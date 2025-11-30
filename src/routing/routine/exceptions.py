"""Exceptions related to routine operations."""

from fastapi import status

from src.app.exceptions import CustomException


class RoutineNotFoundException(CustomException):
    """Exception raised when a routine entry is not found."""

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Routine with ID {routine_id} not found."


class InvalidValuesForRoutineException(CustomException):
    """Exception raised when invalid values are provided for routine creation or update."""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Invalid values provided for routine creation or update."
