from enum import StrEnum, auto

from attrs import define


class PlayType(StrEnum):
    TRAGEDY = auto()
    COMEDY = auto()


@define
class Play:
    name: str
    type: PlayType
