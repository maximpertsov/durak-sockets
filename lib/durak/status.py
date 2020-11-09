from enum import Enum


class Status(Enum):
    COLLECTING = "collecting"
    OUT_OF_PLAY = "out_of_play"
    DURAK = "durak"
    YIELDED = "yielded"
