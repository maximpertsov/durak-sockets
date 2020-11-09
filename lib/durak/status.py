from enum import Enum
from functools import total_ordering


@total_ordering
class Status(Enum):
    COLLECTING = "collecting"
    OUT_OF_PLAY = "out_of_play"
    DURAK = "durak"
    YIELDED = "yielded"

    def __lt__(self, other):
        return self.value < other.value
