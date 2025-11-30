"""Tables related to database operations."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey

from src.database.database import Base


class Music(Base):
    """Database table for music information."""

    __tablename__ = "music"

    music_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)


class Preference(Base):
    """Database table for user preference."""

    __tablename__ = "preference"

    preference_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    music_id = Column(Integer, ForeignKey("music.music_id"), nullable=False)
    led_color = Column(Integer, nullable=False)


class Routine(Base):
    """Database table for routines."""

    __tablename__ = "routine"

    routine_id = Column(Integer, primary_key=True, index=True)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    weekday = Column(Integer, nullable=False)


class Tag(Base):
    """Database table for tags."""

    __tablename__ = "tag"

    tag_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    preference_id = Column(Integer, ForeignKey("preference.preference_id"))
    routine_id = Column(Integer, ForeignKey("routine.routine_id"), nullable=True)
    first_use = Column(String, nullable=False, default=datetime.now().isoformat())
    last_use = Column(String, nullable=False, default=datetime.now().isoformat())


class History(Base):
    """Database table for tag usage history."""

    __tablename__ = "history"

    history_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tag_id = Column(String, ForeignKey("tag.tag_id"), nullable=False)
    timestamp = Column(String, nullable=False, default=datetime.now().isoformat())



preference_table = Preference.__table__
music_table = Music.__table__
routine_table = Routine.__table__
tag_table = Tag.__table__
history_table = History.__table__
