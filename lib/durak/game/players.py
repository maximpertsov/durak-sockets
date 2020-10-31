from operator import attrgetter

from lib.durak.player import Player


class Players:
    @classmethod
    def deserialize(cls, players):
        return cls(
            players_by_id={
                player["id"]: Player.deserialize(player) for player in players
            },
        )

    def __init__(self, *, players_by_id):
        self._players_by_id = players_by_id

    def ordered(self):
        return sorted(self._players_by_id.values(), key=attrgetter("order"))

    def player(self, player_or_id):
        key = player_or_id.id if isinstance(player_or_id, Player) else player_or_id
        return self._players_by_id[key]
