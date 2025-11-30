"""Router for tag-related endpoints."""
from fastapi import APIRouter, status


from src.routing.preference.service import preference_service
from src.routing.preference.schemas import PreferenceRequest
from src.routing.routine.schemas import Routine
from src.routing.routine.service import routine_service
from src.routing.routine.exceptions import InvalidValuesForRoutineException
from src.routing.tags.schemas import TagRequest
from src.routing.tags.service import tag_service

tag_router = APIRouter()
prefix = "/tag"


@tag_router.get(prefix+"/handle", status_code=status.HTTP_201_CREATED)
async def handle_tag_request(
    tag_id: str,
    name: str,
    led_color: int,
    music_id: int,
    routine_id: int = None,
    end_time: str = None,
    start_time: str = None,
    weekday: int = None
) -> None:
    """Endpoint to create or update a tag history.

    Args:
        tag_id (str): The ID of the tag.
        name (str): The name of the tag.
        led_color (int): The LED color associated with the tag.
        music_id (int): The music ID associated with the tag.
        routine_id (int): The routine ID.
        end_time (str, optional): The end time for the routine, if applicable.
        start_time (str, optional): The start time for the routine, if applicable.
        weekday (int, optional): The weekday for the routine, if applicable.

    Raises:
        InvalidValuesForRoutineException: If routine_id is provided but any of
        end_time, start_time, or weekday is missing.
    """
    if routine_id:
        if not end_time or not start_time or not weekday:
            raise InvalidValuesForRoutineException
        routine = Routine(
        routine_id=routine_id,
        start_time=start_time,
        end_time=end_time,
        weekday=weekday,
        )
        await routine_service.handle_routine_request(routine)
    preference_request = PreferenceRequest(
        led_color=led_color,
        music_id=music_id,
    )
    preference = await preference_service.handle_preference_request(
        preference_request)
    tag_request = TagRequest(
        tag_id=tag_id,
        name=name,
        preference_id=preference.preference_id,
        routine_id=routine_id,
    )
    await tag_service.handle_tag_request(tag_request)
    

@tag_router.post(prefix, status_code=status.HTTP_201_CREATED)
async def create_tag(new_tag: TagRequest) -> None:
    """Endpoint to create a new tag.

    Args:
        new_tag (TagRequest): The tag data to create.
    """
    await tag_service.create_tag(new_tag)


@tag_router.get(prefix)
async def get_tag(tag_id: str) -> dict:
    """Endpoint to retrieve a tag by its ID.

    Args:
        id (str): The ID of the tag to retrieve.

    Returns:
        dict: The tag data.
    """
    tag = await tag_service.get_tag_by_id(tag_id)
    preference = await preference_service.get_preference_by_id(
        tag.preference_id)
    response_dict = {
        "led_color": preference.led_color,
        "music_id": preference.music_id,
        "routine_id": None
    }
    if tag.routine_id:
        if await routine_service.check_runnable_routine(tag.routine_id):
            response_dict["routine_id"] = tag.routine_id
    return response_dict
        


@tag_router.get(prefix+"/history")
async def get_tag_history(id: str) -> list[dict]:
    """Endpoint to retrieve the history of a tag by its ID.

    Args:
        id (str): The ID of the tag whose history to retrieve.

    Returns:
        list: The history of the tag.
    """
    return await tag_service.get_tag_history(id)


@tag_router.delete(prefix, status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: str) -> None:
    """Endpoint to delete a tag by its ID.

    Args:
        tag_id (str): The ID of the tag to delete.
    """
    await tag_service.delete_tag(tag_id)
