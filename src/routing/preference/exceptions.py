"""Exceptions for preference operations."""

from fastapi import status

from src.app.exceptions import CustomException


class PreferenceNotFoundException(CustomException):
    """Exception raised when a preference is not found."""

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DEFAULT_DETAIL = "Preference with ID {music_id} and {led_color} not found."


class PreferenceIDNotFoundException(CustomException):
    """Exception raised when a preference is not found by ID."""

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DEFAULT_DETAIL = "Preference with ID {preference_id} not found."


class PreferenceAlreadyExistsException(CustomException):
    """Exception raised when a preference already exists."""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DEFAULT_DETAIL = "Preference with ID {music_id} and {led_color} already exists."
