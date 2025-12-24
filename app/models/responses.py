from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar('T')


class DataResponse(BaseModel, Generic[T]):
    data: T


class ListDataResponse(BaseModel, Generic[T]):
    data: List[T]

