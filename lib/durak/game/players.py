from operator import attrgetter

from lib.durak.player import Player
from lib.durak.status import Status


class Players:
    @classmethod
    def deserialize(cls, players):
        return cls(players=[Player.deserialize(player) for player in players])

    def __init__(self, *, players):
        self._players_by_id = {player.id: player for player in players}

    def serialize(self):
        return [player.serialize() for player in self.ordered()]

    def ordered_in_play(self):
        return [
            player
            for player in self.ordered()
            if not player.has_status(Status.OUT_OF_PLAY)
        ]

    def ordered(self):
        return sorted(self._players_by_id.values(), key=attrgetter("order"))

    def player(self, player_or_id):
        key = player_or_id.id if isinstance(player_or_id, Player) else player_or_id
        return self._players_by_id[key]
