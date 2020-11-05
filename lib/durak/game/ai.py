from itertools import chain
from random import choice

from lib.durak.exceptions import IllegalAction


class AI:
    class CannotPerform(IllegalAction):
        pass

    def __init__(self, *, game):
        self._game = game

    def perform_action(self, *, player):
        """
        Have the user perform a random action.

        Do nothing if yielded.
        """
        _player = self._player(player)
        if self._player(_player) in self._game._yielded.get():
            raise self.CannotPerform("Already yielded")

        selected_action = choice(self._potential_actions(player=_player))
        selected_action(player=_player)

    def _potential_actions(self, *, player):
        # TODO: report action on event?

        defending = player == self._game.defender
        not_defending = not defending

        return list(
            chain(
                [self._attack] * 3 * not_defending,
                # self._pass_card,
                [self._defend] * 9 * defending,
                [self._give_up] * 1 * defending,
                [self._yield_attack] * 7 * not_defending,
            )
        )

    def _attack(self, *, player):
        """
        Throw a random, legal attack card
        """
        try:
            potential_cards = list(
                set(self._game._legal_attacks._cards)
                & set(self._player(player).cards())
            )
            card = choice(potential_cards)
            self._game.legally_attack(player=player, cards=[card])
        except (IllegalAction, IndexError) as error:
            print("Cannot attack", {"player": player.id, "error": error})
            raise self.CannotPerform

    def _yield_attack(self, *, player):
        try:
            self._game.yield_attack(player=player)
        except IllegalAction:
            raise self.CannotPerform

    def _defend(self, *, player):
        """
        Defend randomly
        """
        try:
            base_card, potential_cards = choice(
                list(self._game.legal_defenses._legal_defenses.items())
            )
            if not potential_cards:
                self._game.give_up(player=player)
                return

            card = choice(list(potential_cards))
            self._game.legally_defend(player=player, base_card=base_card, card=card)
        except (IllegalAction, IndexError):
            raise self.CannotPerform

    def _give_up(self, *, player):
        try:
            self._game.give_up(player=player)
        except IllegalAction:
            raise self.CannotPerform

    def serialize(self):
        return [player.serialize() for player in self.ordered()]

    def _player(self, player_or_id):
        return self._game.player(player_or_id)
