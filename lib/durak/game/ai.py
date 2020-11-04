from random import choice

from lib.durak.exceptions import IllegalAction


class AI:
    class CannotPerform(IllegalAction):
        pass

    def __init__(self, *, game):
        self._game = game

    def perform_action(self, *, player):
        """
        Have the user perform a random action
        """
        selected_action = choice(self._potential_actions())
        selected_action(player=self._player(player))

    def _potential_actions(self):
        # TODO: filter out impossible actions?

        return [
            self._attack,
            # self._pass_card,
            # self._defend,
            # self._give_up,
            # self._yield_attack,
            # self._do_nothing,
        ]

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
            base_card, card = choice(
                [
                    (base_card, choice(cards))
                    for base_card, cards in self._game._legal_defenses._legal_defenses.items()
                ]
            )
        except (IllegalAction, IndexError):
            raise self.CannotPerform

    def serialize(self):
        return [player.serialize() for player in self.ordered()]

    def _player(self, player_or_id):
        return self._game.player(player_or_id)
