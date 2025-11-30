"""Service related to routine operations."""

from datetime import datetime

from src.database.database import Database
from src.database.tables import routine_table
from src.routing.routine.schemas import Routine
from src.routing.routine.exceptions import RoutineNotFoundException
from src.routing.routine.utils import RoutineUtils, routine_config


class RoutineService:
    """Service class for routine operations."""

    @classmethod
    async def handle_routine_request(cls, routine: Routine) -> None:
        """Handle routine request.

        Args:
            routine (Routine): The routine data.
        """
        if not await cls.routine_exists(routine.routine_id):
            await cls.create_routine(routine)
            return
        await cls.update_routine(routine)

    @classmethod
    async def create_routine(cls, routine: Routine) -> None:
        """Create a new routine in the database.
        
        Args:
            routine (Routine): The routine data to be created.
        """

        query = routine_table.insert().values(
            routine_id=routine.routine_id,
            start_time=routine.start_time,
            end_time=routine.end_time,
            weekday=routine.weekday
        )
        await Database.execute(query)

    @classmethod
    async def get_routine(cls, routine_id: int) -> Routine:
        """Retrieve a routine from the database by its ID.

        Args:
            routine_id (int): The ID of the routine to retrieve.

        Returns:
            Routine: The retrieved routine data.

        Raises:
            RoutineNotFoundException: If the routine does not exist.
        """
        query = routine_table.select().where(routine_table.c.routine_id == routine_id)
        result = await Database.fetch_one(query)
        if result is None:
            raise RoutineNotFoundException(routine_id=routine_id)
        return Routine(**result)

    @classmethod
    async def update_routine(cls, routine: Routine) -> None:
        """Update an existing routine in the database.

        Args:
            routine (Routine): The routine data to be updated.
        """
        query = (
            routine_table.update()
            .where(routine_table.c.routine_id == routine.routine_id)
            .values(
                start_time=routine.start_time,
                end_time=routine.end_time,
                weekday=routine.weekday
            )
        )
        await Database.execute(query)

    @classmethod
    async def check_runnable_routine(cls, routine_id: int) -> bool:
        """Check if a routine is runnable based on its ID.

        Args:
            routine_id (int): The ID of the routine to check.

        Returns:
            bool: True if the routine is runnable, False otherwise.
        """
        routine = await cls.get_routine(routine_id)
        today = RoutineUtils.get_weekday()
        hour_now = datetime.now().hour - routine_config.HOURS_ADJUST
        if hour_now < 0:
            hour_now += 24
            today -= 1
        minute_now = datetime.now().minute
        if routine.weekday != today:
            return False
        splitted_start_time = routine.start_time.strip().split(":")
        splitted_end_time = routine.end_time.strip().split(":")
        start_hour = int(splitted_start_time[0])
        end_hour = int(splitted_end_time[0])
        if (start_hour > hour_now) or (end_hour < hour_now):
            return False
        if hour_now == end_hour:
            end_minute = int(splitted_end_time[1])
            if not (minute_now <= end_minute):
                return False
        return True

    @classmethod
    async def routine_exists(cls, routine_id: int) -> bool:
        """Check if a routine exists in the database.

        Args:
            routine_id (int): The ID of the routine to check.

        Returns:
            bool: True if the routine exists, False otherwise.
        """
        query = routine_table.select().where(routine_table.c.routine_id == routine_id)
        result = await Database.fetch_one(query)
        return result is not None


routine_service = RoutineService()
