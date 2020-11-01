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

    def update(self, *, player):
        if self._game.player(player).cards():
            return
        if self._game._draw_pile.size():
            return

        self._game.player(player).add_status(Status.WINNER)

        # TODO: check if durak
