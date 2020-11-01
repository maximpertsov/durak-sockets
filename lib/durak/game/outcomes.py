from lib.durak.status import Status
from lib.durak.exceptions import IllegalAction


class Outcomes:
    class MultipleDuraks(IllegalAction):
        pass

    def __init__(self, *, game):
        self._game = game

    def get_winners(self):
        return set(
            [
                player
                for player in self._game.ordered_players()
                if player.has_status(Status.WINNER)
            ]
        )

    def get_durak(self):
        for player in self._game.ordered_players():
            if player.has_status(Status.DURAK):
                return player

    def get_active(self):
        result = set(self._game.ordered_players())
        result.difference_update(self.get_winners())
        result.difference_update(set([self.get_durak()]))
        return result

    def update(self, *, player):
        if self.get_durak():
            return
        if self._game.player(player).cards():
            return
        if self._game._draw_pile.size():
            return

        if len(self.get_active()) > 1:
            self._game.player(player).add_status(Status.WINNER)

        active_players = self.get_active()
        if len(active_players) == 1:
            self._set_durak(player=active_players.pop())

    def _set_durak(self, *, player):
        if self.get_durak():
            raise self.MultipleDuraks

        self._game.player(player).add_status(Status.DURAK)
