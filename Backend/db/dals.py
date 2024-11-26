from typing import Union
from uuid import UUID

from sqlalchemy import and_, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Event, User


class EventDAL:
    def __init__(self, db_session=AsyncSession):
        self.db_session = db_session

    async def create_event(self, event_name: str, place: str, short_description: str, long_description: str, max_count_of_members: int,
                           online_event_link:str, format: str, tags: str) -> Event:
        new_event = Event(
            event_name=event_name,
            place=place,
            short_description=short_description,
            long_description=long_description,
            max_count_of_members=max_count_of_members,
            online_event_link=online_event_link,
            format = format,
            tags=tags
)
        self.db_session.add(new_event)
        await self.db_session.flush()
        return new_event

    async def archive_event(self, event_id: int) -> Union[Event, None]:
        query = update(Event).where(and_(Event.event_id == event_id, Event.is_active == True)).values(
            is_active=False).returning(Event.event_id)
        res = await self.db_session.execute(query)
        # res.fetchone(): Извлекает первую строку результата запроса.
        archive_event_id_row = res.fetchone()
        if archive_event_id_row is not None:
            return archive_event_id_row[0]

    async def update_event(self, event_id: int, **kwargs) -> Union[Event, None]:
        query = update(Event).where(Event.event_id == event_id).values(kwargs).returning(
            Event.event_id)
        res = await self.db_session.execute(query)
        updated_event_id_row = res.fetchone()
        if updated_event_id_row is not None:
            return updated_event_id_row[0]

    async def get_event_by_id(self, event_id: int) -> Union[Event, None]:
        query = select(Event).where(Event.event_id == event_id)
        res = await self.db_session.execute(query)
        event_row = res.fetchone()
        if event_row is not None:
            return event_row[0]


class UserDAL:
    def __init__(self, db_session=AsyncSession):
        self.db_session = db_session

    async def create_user(
        self, name: str, surname: str, email: str, hashed_password: str, age: int,
        course: int, university_group: str) -> User:
        new_user = User(
            name=name, surname=surname, email=email, hashed_password=hashed_password, role="user", age=age,
            course=course, university_group=university_group
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def update_user(self, user_id: int, **kwargs) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id))
            .values(kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

class AdminDAL():
    def __init__(self, db_session=AsyncSession):
        self.db_session = db_session

    async def create_admin(
            self, name: str, surname: str, email: str, hashed_password: str, age: int = None,
            course: int = None, university_group: str = None) -> User:
        new_user = User(
            name=name, surname=surname, email=email, hashed_password=hashed_password, role="admin", age=age,
            course=course, university_group = university_group
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user


