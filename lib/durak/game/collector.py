from lib.durak.exceptions import IllegalAction
from lib.durak.status import Status


class Collector:
    class MultipleCollectors(IllegalAction):
        pass

    def __init__(self, *, game, player=None):
        self._game = game
        if player is not None:
            self.set(player=player)

    def __bool__(self):
        return bool(self.get())

    def get(self):
        for player in self._game._ordered_players():
            if not player.has_status(Status.COLLECTING):
                continue

            return player

    def set(self, *, player):
        if self:
            raise self.MultipleCollectors

        self._player(player).add_status(Status.COLLECTING)

    def clear(self):
        if (collector := self.get()) :
            collector.remove_status(Status.COLLECTING)

    def _player(self, player_or_id):
        if isinstance(player_or_id, (str, int)):
            return self._game._player(player_or_id)
        return player_or_id
