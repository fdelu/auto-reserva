from typing import Annotated, Any, TypeVar, Generic
from datetime import time

from pydantic import (
    BaseModel,
    NaiveDatetime,
    Field,
    AliasChoices,
    AliasPath,
    BeforeValidator,
    field_validator,
    TypeAdapter,
)
from pydantic.alias_generators import to_camel
from pydantic_extra_types.timezone_name import TimeZoneName


T = TypeVar("T")


class OndeporResponse(BaseModel, Generic[T]):
    status: str
    status_code: int | None = None
    data: Annotated[T, Field(validation_alias=AliasChoices("data", "model"))]

    model_config = {"populate_by_name": True, "alias_generator": to_camel}


# Players


class Player(BaseModel):
    id: Annotated[int, Field(alias="player_id")]
    firstname: Annotated[str, Field(alias="firstname_player")]
    lastname: Annotated[str, Field(alias="lastname_player")]

    model_config = {"populate_by_name": True}


PlayerListTA = TypeAdapter(list[Player])

# Courts


class Court(BaseModel):
    name: str
    court_name: str


# Reservations


class CourtReservation(Court):
    time_to: str


class Reservation(BaseModel):
    id: int
    club_reservation_id: int
    reservation_date_from: NaiveDatetime
    reservation_date_to: NaiveDatetime
    players: list[Player]
    court: CourtReservation


class ReservationList(BaseModel):
    reservations: list[Reservation]


# Clubs


class Club(BaseModel):
    id: int
    name: str
    logo: Annotated[
        str,
        Field(validation_alias=AliasChoices("logo", AliasPath("sports", "image_url"))),
    ]
    timezone: TimeZoneName | None = None
    club_childs: Annotated[list["Club"], Field(default_factory=list)] = []


class ClubList(BaseModel):
    clubs_mains: list[Club]


# Calendar


class CourtCalendar(BaseModel):
    id: int


class CalendarReservation(BaseModel):
    id: int
    text: str
    title: str
    rowspan: int
    players_ids: list[int]

    @field_validator("text", mode="after")
    def format_text(cls, v: str) -> str:
        return "; ".join(name.strip() for name in v.split("<br>"))

    @field_validator("players_ids", mode="before")
    def validate_players(cls, v: Any) -> Any:
        if not isinstance(v, list):
            return v
        return [p for p in v if p != ""]  # type: ignore


class CalendarReservationRowspan(BaseModel):
    id: int


def filter_restricted_hour(v: Any) -> Any:
    """Remove 'restricted_hour' keys from each time slot dictionary."""
    if not isinstance(v, dict):
        return v

    return {k: val for k, val in v.items() if k != "restricted_hour"}  # type: ignore


def check_slot_available(v: Any) -> Any:
    if isinstance(v, dict):
        if "id" in v and v["id"] == 0:
            return None
        if "is_rowspan" in v and v["is_rowspan"] is True:
            return CalendarReservationRowspan.model_validate(v)

    return v  # type: ignore


class Calendar(BaseModel):
    today: NaiveDatetime
    hour_from: time
    hour_to: time
    courts: list[CourtCalendar]
    calendar_grid: dict[
        time,
        Annotated[
            dict[
                str,
                Annotated[
                    CalendarReservation | CalendarReservationRowspan | None,
                    BeforeValidator(check_slot_available),
                ],
            ],
            BeforeValidator(filter_restricted_hour),
        ],
    ]
    my_reservations: list[int]
