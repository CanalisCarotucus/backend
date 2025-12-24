from fastapi import APIRouter

from app.models.hello_world import HelloWorldData
from app.models.items import ItemsData
from app.models.responses import DataResponse

router = APIRouter()


@router.get("/")
async def hello_world():
    return DataResponse(data={"message": "Hello World!"})


@router.post("/data")
async def hello_world_data(data: HelloWorldData):
    return {"message": "Hello World!", "data": data.some_data.strip()}
