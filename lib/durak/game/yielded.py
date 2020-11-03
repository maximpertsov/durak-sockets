from lib.durak.status import Status
from lib.durak.exceptions import IllegalAction


class Yielded:
    class YieldOutOfTurn(IllegalAction):
        pass

    def __init__(self, *, game):
        self._game = game

    def __bool__(self):
        return bool(self.get())

    def get(self):
        return set(
            [
                player
                for player in self._game.ordered_players()
                if player.has_status(Status.YIELDED)
            ]
        )

    def add(self, *, player):
        if self._game.player(player) == self._game._defender():
            raise self.YieldOutOfTurn

        self._game.player(player).add_status(Status.YIELDED)

    def clear(self):
        for player in self._game.ordered_players():
            player.remove_status(Status.YIELDED)
