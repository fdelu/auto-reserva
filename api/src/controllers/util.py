from typing import Annotated

from httpx import AsyncClient
import jwt
from fastapi import Cookie

from .ondepor import OndeporClient

SECRET_KEY = "your-super-secret-key"


# TODO add to_async


async def get_cookies_jwt(http_client: AsyncClient):
    cookies = {name: http_client.cookies.get(name) for name in http_client.cookies}
    token: str = jwt.encode(cookies, SECRET_KEY, algorithm="HS256")  # type: ignore
    return token


async def decode_cookies_jwt(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


async def get_ondepor_session(ondepor_session: Annotated[str, Cookie()]):
    async with AsyncClient() as http_client:
        cookies = await decode_cookies_jwt(ondepor_session)
        http_client.cookies.update(cookies)
        yield OndeporClient(http_client)
