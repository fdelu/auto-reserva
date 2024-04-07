from typing import Literal

from fastapi import APIRouter, Depends

from .log import AppLogger

router = APIRouter()


@router.get("/health", tags=["Healthcheck"])
def health_check(log: AppLogger = Depends()) -> Literal["OK"]:
    log.debug("Health check successful")
    return "OK"
