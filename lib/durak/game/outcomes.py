from lib.durak.status import Status


class Outcomes:
    def __init__(self, *, game):
        self._game = game

    def __bool__(self):
        return bool(self.get())

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
        return set(self._game.ordered_players()) - self.get_winners()

    def update(self, *, player):
        if self._game.player(player).cards():
            return
        if self._game._draw_pile.size():
            return

        self._game.player(player).add_status(Status.WINNER)

        active_players = self.get_active()
        if len(active_players) == 1:
            self._game.player(active_players.pop()).add_status(Status.DURAK)
