"""Service module for tag-related operations."""

from sqlalchemy.exc import IntegrityError

from src.database.database import Database
from src.database.tables import tag_table, history_table
from src.routing.tags.exceptions import (
    TagAlreadyExistsException,
    TagNotFoundException
)
from src.routing.tags.schemas import TagRequest, TagResponse
from src.routing.tags.utils import TagUtils


class TagService:
    """Service class for tag operations."""

    @classmethod
    async def handle_tag_request(cls, tag: TagRequest) -> None:
        """Handle tag request.
        
        Args:
            tag (str): The tag data.
        """
        if not await cls.tag_exists(tag.tag_id):
            await cls.create_tag(tag)
            return
        await cls.update_tag_by_id(tag)

    @classmethod
    async def create_tag(cls, new_tag: TagRequest) -> None:
        """Create a new tag.

        Args:
            new_tag (TagRequest): The tag data to create.

        Raises:
            TagAlreadyExistsException: If a tag with the same ID already exists.
        """
        try:
            timestamp = TagUtils.get_timestamp()
            tag_query = tag_table.insert().values(
                tag_id=new_tag.tag_id,
                name=new_tag.name,
                preference_id=new_tag.preference_id,
                routine_id=new_tag.routine_id,
                first_use=timestamp,
                last_use=timestamp
            )
            history_query = history_table.insert().values(
                tag_id=new_tag.tag_id, timestamp=timestamp)
            await Database.execute_many([tag_query, history_query])
        except IntegrityError:
            raise TagAlreadyExistsException(id=new_tag.tag_id)

    @classmethod
    async def get_tag_by_id(cls, tag_id: str) -> dict:
        """Retrieve a tag by its ID.

        Args:
            tag_id (str): The ID of the tag to retrieve.

        Raises:
            TagNotFoundException: If the tag with the specified ID does not exist.

        Returns:
            dict: The tag data.
        """
        query = tag_table.select().where(tag_table.c.tag_id == tag_id)
        tag = await Database.fetch_one(query)
        if not tag:
            raise TagNotFoundException(id=tag_id)
        return TagResponse(**tag)

    @classmethod
    async def get_tag_history(cls, id: str) -> list[dict]:
        """Retrieve the history of a tag by its ID.

        Args:
            id (str): The ID of the tag whose history to retrieve.

        Raises:
            TagNotFoundException: If the tag with the specified ID does not exist.

        Returns:
            list: The history of the tag.
        """
        await cls.get_tag_by_id(id)  # Ensure tag exists
        query = history_table.select().where(history_table.c.tag_id == id)
        return await Database.fetch_all(query)

    @classmethod
    async def update_tag_by_id(cls, data: TagRequest) -> None:
        """Update a tag by its ID.

        Args:
            data (TagRequest): The tag data to update.

        Raises:
            TagNotFoundException: If the tag with the specified ID does not exist.
        """
        await cls.get_tag_by_id(data.tag_id)  # Ensure tag exists
        timestamp = TagUtils.get_timestamp()
        tag_query = tag_table.update().where(tag_table.c.tag_id == data.tag_id).values(
            preference_id=data.preference_id,
            routine_id=data.routine_id,
            last_use=timestamp
        )
        history_query = history_table.insert().values(
            tag_id=data.tag_id, timestamp=timestamp
        )
        await Database.execute_many([tag_query, history_query])

    @classmethod
    async def delete_tag(cls, tag_id: str) -> None:
        """Delete a tag by its ID.

        Args:
            tag_id (str): The ID of the tag to delete.

        Raises:
            TagNotFoundException: If the tag with the specified ID does not exist.
        """
        query = tag_table.delete().where(tag_table.c.tag_id == tag_id)
        await Database.execute(query)

    @classmethod
    async def tag_exists(cls, tag_id: str) -> bool:
        """Check if a tag exists by its ID.

        Args:
            tag_id (str): The ID of the tag to check.
        
        Returns:
            bool: True if the tag exists, False otherwise.
        """
        query = tag_table.select().where(tag_table.c.tag_id == tag_id)
        tag = await Database.fetch_one(query)
        return tag is not None


tag_service = TagService()
