from pydantic import BaseModel, Field
from typing import List


class ItemsData(BaseModel):
    some_data: List[str] = Field(..., min_length=1)

