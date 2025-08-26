import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from asyncio import sleep
from typing import Any, no_type_check
import logging

from httpx import AsyncClient
from bs4 import BeautifulSoup, Tag

from .models import OndeporResponse, ReservationList, ClubList, Calendar, PlayerListTA

ONDEPOR_URL = "https://www.ondepor.com"
TOO_EARLY_ERROR_REGEX = re.compile(
    r"Este club permite reservar para ese día a partir de las \d+:\d+ horas."
)
ERROR_LINE_BREAK_REGEX = re.compile(r"(<br>| )+")


@dataclass
class CSRFMetadata:
    param: str
    token: str


class OndeporClient:
    http_client: AsyncClient
    logger: logging.Logger

    def __init__(self, http_client: AsyncClient):
        self.http_client = http_client
        self.logger = logging.getLogger("app.ondepor")

    def __soup_get(self, soup: BeautifulSoup, kind: str, name: str, key: str):
        tag = soup.find(kind, {"name": name})
        if not isinstance(tag, Tag):
            raise ValueError(f"{kind} with name {name} not found")
        value = tag[key]
        if isinstance(value, str):
            return value
        return " ".join(value)

    async def __get_csrf_metadata(self, url: str = ONDEPOR_URL):
        r = await self.http_client.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        return CSRFMetadata(
            param=self.__soup_get(soup, "meta", "csrf-param", "content"),
            token=self.__soup_get(soup, "meta", "csrf-token", "content"),
        )

    async def login(self, username: str, password: str):
        self.logger.info("Logging in to Ondepor")

        csrf = await self.__get_csrf_metadata()
        r = await self.http_client.get(f"{ONDEPOR_URL}/site/login-modal")
        r.raise_for_status()
        soup = BeautifulSoup(r.json()["div"], "html.parser")
        login_csrf = self.__soup_get(soup, "input", csrf.param, "value")

        r = await self.http_client.post(
            f"{ONDEPOR_URL}/site/login",
            data={
                csrf.param: login_csrf,
                "LoginForm[email]": username,
                "LoginForm[password]": password,
            },
            headers={"X-CSRF-Token": csrf.token, "x-requested-with": "XMLHttpRequest"},
        )
        r.raise_for_status()

        self.logger.info("Successfully logged in to Ondepor")

    async def get_user_reservations(self):
        response = await self.http_client.get(
            f"{ONDEPOR_URL}/player/reservation/list?all=1"
        )
        response.raise_for_status()
        return (
            OndeporResponse[ReservationList]
            .model_validate_json(response.text)
            .data.reservations
        )

    async def get_user_clubs(self):
        response = await self.http_client.get(f"{ONDEPOR_URL}/player/club/favorites")
        response.raise_for_status()
        return (
            OndeporResponse[ClubList]
            .model_validate_json(response.text)
            .data.clubs_mains
        )

    async def get_calendar(self, club_id: int, date: date):
        csrf = await self.__get_csrf_metadata(f"{ONDEPOR_URL}/user/_favorites")

        # convert to datetime at 00:00
        dt = datetime.combine(date, datetime.min.time())
        epoch_timestamp = int(dt.timestamp())
        response = await self.http_client.post(
            f"{ONDEPOR_URL}/player/calendar/detail/index",
            data={
                "time": epoch_timestamp,
                "club_id": club_id,
                "offset": 0,
                "svid": "2.1.1",
            },
            headers={"X-CSRF-Token": csrf.token, "x-requested-with": "XMLHttpRequest"},
        )
        response.raise_for_status()
        return OndeporResponse[Calendar].model_validate_json(response.text).data

    async def make_reservation(self):
        csrf = await self.__get_csrf_metadata(f"{ONDEPOR_URL}/user/_favorites")

        start = datetime.combine(date(2025, 8, 24), time(16, 0))
        end = start + timedelta(hours=1)

        club = 172
        court = 1053
        time_start = start.strftime("%H:%M")
        time_end = end.strftime("%H:%M")

        midnight = datetime.combine(start.date(), datetime.min.time())
        epoch_midnight = int(midnight.timestamp())

        doubles = False
        vanina_player_id = 86906

        # Obtain jid
        r = await self.http_client.post(
            f"{ONDEPOR_URL}/player/reservation/my-reservation-new",
            data={
                "id": f"time-{time_start}-club-{club}-{epoch_midnight}",
                "date_from": start.date().isoformat(),
                "svid": "2.1.1",
            },
            headers={"X-CSRF-Token": csrf.token, "x-requested-with": "XMLHttpRequest"},
        )
        r.raise_for_status()
        result = r.json()
        check_request_result(result, "add reservation")

        model = result["model"]
        jid = model["jid"]
        telephone = model["reservation_form"]["fields"]["field_telephone"]["value"]

        await sleep(0.25)  # Without this it sometimes returns an unknown error

        r = await self.http_client.post(
            f"{ONDEPOR_URL}/player/reservation/add-reservation-new",
            data={
                "ReservationForm[single_double]": 2 if doubles else 1,
                "ReservationForm[time_from]": time_start,
                "ReservationForm[time_to]": time_end,
                "ReservationForm[court_id]": court,
                "ReservationForm[telephone]": telephone,
                "ReservationForm[remember]": 0,
                "ReservationForm[club_id]": club,
                "ReservationForm[date]": start.date().isoformat(),
                "ReservationForm[jid]": jid,
                "player_id[1]": vanina_player_id,
                "invitations": 0,
                "svid": "2.1.1",
            },
            headers={"X-CSRF-Token": csrf.token, "x-requested-with": "XMLHttpRequest"},
        )
        r.raise_for_status()
        check_request_result(r.json(), "add reservation")

    async def cancel_reservation(self, reservation_id: int):
        csrf = await self.__get_csrf_metadata(f"{ONDEPOR_URL}/user/_favorites")

        r = await self.http_client.post(
            f"{ONDEPOR_URL}/player/reservation/cancel-reservation",
            data={
                "CancelReservationForm[id]": reservation_id,
                "CancelReservationForm[delete_reservation_all]": False,
                "CancelReservationForm[delete_reservation_group_all]": False,
                "from_next_matches": ".$from_next_matches.",
                "g-recaptcha-response": "undefined",
                "svid": "2.1.1",
            },
            headers={"X-CSRF-Token": csrf.token, "x-requested-with": "XMLHttpRequest"},
        )
        r.raise_for_status()
        check_request_result(r.json(), "cancel reservation")

    async def get_players(self, club_id: int, query: str):
        csrf = await self.__get_csrf_metadata(f"{ONDEPOR_URL}/user/_favorites")

        r = await self.http_client.get(
            f"{ONDEPOR_URL}/player/reservation/search-players",
            params={"club_id": club_id, "q": query, "svid": "2.1.1"},
            headers={"X-CSRF-Token": csrf.token, "x-requested-with": "XMLHttpRequest"},
        )
        r.raise_for_status()
        self.logger.critical(f"result: {r.text}")
        return PlayerListTA.validate_json(r.text)


def check_request_result(result: dict[str, Any], message: str):
    if result["status"] == "success":
        return
    print(result)
    error = result.get("result_text") or result.get("errors") or result.get("message")
    print(error)
    error = get_error_msg(error)
    print(error)
    error = re.sub(ERROR_LINE_BREAK_REGEX, " ", error).strip()
    print(error)
    if re.match(TOO_EARLY_ERROR_REGEX, error):
        raise RuntimeError(f"Too early to make reservation: {error}")
    raise ValueError(f"Failed to {message}: {error}")


@no_type_check
def get_error_msg(error: Any) -> str:
    if isinstance(error, str):
        return error
    if isinstance(error, list):
        return get_error_msg(error[0]) if len(error) > 0 else "Unknown error"
    if not isinstance(error, dict):
        return "Unknown error"
    keys = list[Any](error.keys())
    if len(keys) != 1:
        return "Unknown error"
    return get_error_msg(error[keys[0]])
