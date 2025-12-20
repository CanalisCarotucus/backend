from loguru import logger
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import text

from app.middlewares.log import log_middle
from app.config.config import settings
from app.routers import api, v1, v2
from app.database.connection import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    try:
        async with engine.begin() as conn:
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


app.add_middleware(BaseHTTPMiddleware, dispatch=log_middle)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTION", "DELETE", "PUT", "PATCH", "HEAD"],
    allow_headers=["*"],
)

app.include_router(api.router)
app.include_router(v1.router)
app.include_router(v2.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug",
    )
