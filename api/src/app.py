from contextlib import asynccontextmanager

from fastapi import FastAPI

from .router import router
from .log import setup_logs


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    setup_logs()
    yield


app = FastAPI(lifespan=app_lifespan, title="Auto reservation API", root_path="/api")
app.include_router(router)
