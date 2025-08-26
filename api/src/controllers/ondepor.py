from typing import Annotated

from httpx import AsyncClient
from fastapi import APIRouter, Depends, Response

from ..services.ondepor import OndeporClient, Player
from .util import get_cookies_jwt, get_ondepor_session


router = APIRouter(prefix="/ondepor", tags=["Ondepor"])


@router.get("/players")
async def get_players(
    ondepor: Annotated[OndeporClient, Depends(get_ondepor_session)],
) -> list[Player]:
    return await ondepor.get_players(club_id=172, query="vanina")


@router.post("/login")
async def login(username: str, password: str, response: Response):
    async with AsyncClient() as http_client:
        client = OndeporClient(http_client)
        await client.login(username, password)
        session = await get_cookies_jwt(http_client)
        response.set_cookie("ondepor_session", session)
        return session
