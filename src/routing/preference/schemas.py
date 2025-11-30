"""Schemas for preference operations."""

from pydantic import BaseModel


class PreferenceRequest(BaseModel):
    """Schema for preference."""

    music_id: int
    led_color: int


class Preference(PreferenceRequest):
    """Schema for preference response."""

    preference_id: int
