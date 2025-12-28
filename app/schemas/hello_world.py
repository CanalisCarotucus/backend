from pydantic import BaseModel


class HelloWorldData(BaseModel):
    some_data: str

