from fastapi import APIRouter

from app.models.hello_world import HelloWorldData
from app.models.responses import DataResponse

router = APIRouter(tags=["hello"])


@router.get("/")
async def hello_world():
    return DataResponse(data={"message": "Hello World!"})


@router.post("/data", response_model=DataResponse[dict])
async def hello_world_data(data: HelloWorldData):
    return DataResponse(
        data={"message": "Hello World!", "data": data.some_data.strip()}
    )
