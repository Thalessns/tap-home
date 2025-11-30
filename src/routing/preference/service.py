"""Service related to preference operations."""

from sqlalchemy import and_

from src.database.database import Database
from src.database.tables import preference_table
from src.routing.preference.schemas import Preference, PreferenceRequest
from src.routing.preference.exceptions import (
    PreferenceNotFoundException,
    PreferenceIDNotFoundException,
    PreferenceAlreadyExistsException
)


class PreferenceService:
    """Service class for preference operations."""

    @classmethod
    async def handle_preference_request(cls, preference: PreferenceRequest) -> Preference:
        """Handle preference request.

        Args:
            preference (PreferenceRequest): The preference data.
        """
        if not await cls.preference_exists(preference.music_id, preference.led_color):
            await cls.create_preference(preference)
        return await cls.get_preference(preference.music_id, preference.led_color)

    @classmethod
    async def create_preference(cls, preference: PreferenceRequest) -> None:
        """Create a new preference in the database.

        Args:
            preference (PreferenceRequest): The preference data to be created.

        Raises:
            PreferenceAlreadyExistsException: If the preference already exists.
        """
        if await cls.preference_exists(preference.music_id, preference.led_color):
            raise PreferenceAlreadyExistsException(
                music_id=preference.music_id,
                led_color=preference.led_color
            )
        query = preference_table.insert().values(
            music_id=preference.music_id,
            led_color=preference.led_color
        )
        await Database.execute(query)

    @classmethod
    async def get_preference_by_id(cls, preference_id: int) -> Preference:
        """Retrieve a preference from the database by its ID.

        Args:
            preference_id (int): The ID of the preference.

        Returns:
            Preference: The retrieved preference data.

        Raises:
            PreferenceIDNotFoundException: If the preference does not exist.
        """
        query = preference_table.select().where(
            preference_table.c.preference_id == preference_id
        )
        result = await Database.fetch_one(query)
        if result is None:
            raise PreferenceIDNotFoundException(preference_id=preference_id)
        return Preference(**result)

    @classmethod
    async def get_preference(cls, music_id: int, led_color: int) -> Preference:
        """Retrieve a preference from the database by its music ID and LED color.

        Args:
            music_id (int): The music ID of the preference.
            led_color (int): The LED color of the preference.

        Returns:
            Preference: The retrieved preference data.

        Raises:
            PreferenceNotFoundException: If the preference does not exist.
        """
        query = preference_table.select().where(
            and_(
                preference_table.c.music_id == music_id,
                preference_table.c.led_color == led_color
            )
        )
        result = await Database.fetch_one(query)
        if result is None:
            raise PreferenceNotFoundException(
                music_id=music_id,
                led_color=led_color
            )
        return Preference(**result)

    @classmethod
    async def get_all_preferences(cls) -> list[Preference]:
        """Retrieve all preferences from the database.

        Returns:
            list[Preference]: A list of all preferences.
        """
        query = preference_table.select()
        results = await Database.fetch_all(query)
        return [Preference(**result) for result in results]

    @classmethod
    async def preference_exists(cls, music_id: int, led_color: int) -> bool:
        """Check if a preference exists in the database.

        Args:
            music_id (int): The music ID of the preference.
            led_color (int): The LED color of the preference.

        Returns:
            bool: True if the preference exists, False otherwise.
        """
        query = preference_table.select().where(
            and_(
                preference_table.c.music_id == music_id,
                preference_table.c.led_color == led_color
            )
        )
        result = await Database.fetch_one(query)
        return result is not None


preference_service = PreferenceService()
