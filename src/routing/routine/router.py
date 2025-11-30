"""Router for routine-related operations."""

from fastapi import APIRouter, status

from src.routing.routine.schemas import Routine
from src.routing.routine.service import RoutineService

prefix = "/routine"
routine_router = APIRouter()


@routine_router.post(prefix, status_code=status.HTTP_201_CREATED)
async def create_routine(routine: Routine) -> None:
    """Create a new routine.
    
    Args:
        routine (Routine): The routine data to create.
    """
    await RoutineService.create_routine(routine)


@routine_router.get(prefix, response_model=Routine)
async def get_routines_by_tag(routine_id: str) -> Routine:
    """Get routines by id.
    
    Args:
        routine_id (str): The ID of the routine.

    Returns:
        Routine: The routine data.
    """
    return await RoutineService.get_routine(routine_id)
