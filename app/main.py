from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import text

from app.middlewares.log import log_middle
from app.config.config import settings
from app.api import users, passports, hello_world
from app.db.connection import engine
from app.core.exceptions import BaseAppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Database connection failed: {type(e).__name__}: {e}")
        logger.warning("Application will continue, but database operations may fail")
    try:
        yield
    finally:
        logger.info("Shutting down...")
        await engine.dispose()


app = FastAPI(
    lifespan=lifespan, docs_url=settings.docs_url, redoc_url=settings.redoc_url
)


@app.exception_handler(BaseAppException)
async def app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


app.add_middleware(BaseHTTPMiddleware, dispatch=log_middle)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTION", "DELETE", "PUT", "PATCH", "HEAD"],
    allow_headers=["*"],
)

app.include_router(hello_world.router)
app.include_router(users.router)
app.include_router(passports.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug",
    )
