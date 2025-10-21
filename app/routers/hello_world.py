from fastapi import APIRouter, Request

from app.models.hello_world import HelloWorldData

router = APIRouter()


@router.get("/")
async def hello_world():
    return {"message": "Hello World!"}


@router.post("/data")
async def hello_world_data(request: Request, data: HelloWorldData):
    data = data.some_data.strip()

    return {"message": "Hello World!", "data": data}
