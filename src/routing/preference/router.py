"""Router for preference operations."""

from fastapi import APIRouter, status

from src.routing.preference.schemas import PreferenceRequest, Preference
from src.routing.preference.service import preference_service

prefix = "/preference"
preference_router = APIRouter()


@preference_router.post(prefix, status_code=status.HTTP_201_CREATED)
async def create_preference(preference: PreferenceRequest) -> None:
    """Endpoint to create a new preference.

    Args:
        preference (PreferenceRequest): The preference data to be created.
    """
    await preference_service.create_preference(preference)


@preference_router.get(prefix, response_model=Preference)
async def get_preference(
    music_id: int,
    led_color: int
) -> Preference:
    """Endpoint to retrieve a preference by music ID and LED color.

    Args:
        music_id (int): The music ID of the preference.
        led_color (int): The LED color of the preference.

    Returns:
        Preference: The retrieved preference data.
    """
    return await preference_service.get_preference(music_id, led_color)


@preference_router.get(prefix + "s", response_model=list[Preference])
async def get_preferences() -> list[Preference]:
    """Endpoint to handle multiple preference requests.

    Returns:
        list[Preference]: List of retrieved or created preference data.
    """
    return await preference_service.get_all_preferences()
