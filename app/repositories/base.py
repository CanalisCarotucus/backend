from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        pass

    @abstractmethod
    async def create(self, entity_data: dict) -> T:
        pass

    @abstractmethod
    async def update(self, entity_id: int, entity_data: dict) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, entity_id: int) -> bool:
        pass

