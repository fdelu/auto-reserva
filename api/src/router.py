from typing import Literal
import logging

from fastapi import APIRouter

from .controllers.ondepor import router as ondepor_router

router = APIRouter()


@router.get("/health", tags=["Healthcheck"])
def health_check() -> Literal["OK"]:
    logging.getLogger("app").debug("Health check successful")
    return "OK"


router.include_router(ondepor_router)
