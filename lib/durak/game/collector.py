from lib.durak.exceptions import IllegalAction
from lib.durak.status import Status


class Collector:
    class GiveUpOutOfTurn(IllegalAction):
        pass

    class MultipleCollectors(IllegalAction):
        pass

    class NoAttackCards(IllegalAction):
        pass

    def __init__(self, *, game):
        self._game = game

    def __bool__(self):
        return bool(self.get())

    def get(self):
        for player in self._game.ordered_players():
            if not player.has_status(Status.COLLECTING):
                continue

            return player

    def set(self, *, player):
        if self:
            raise self.MultipleCollectors

        if self._game.player(player) != self._game.defender:
            raise self.GiveUpOutOfTurn

        if not self._game._table.cards():
            raise self.NoAttackCards

        self._game.player(player).add_status(Status.COLLECTING)

    def clear(self):
        if (collector := self.get()) :
            collector.remove_status(Status.COLLECTING)
