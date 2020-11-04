from lib.durak.exceptions import IllegalAction


class LegalDefenses:
    class DefendingAfterGivingUp(IllegalAction):
        pass

    class DefendingAsDurak(IllegalAction):
        pass

    class DefendingWithOutOfHandCard(IllegalAction):
        pass

    class DefendingOutOfTurn(IllegalAction):
        pass

    class NoBaseCard(IllegalAction):
        pass

    class InvalidDefense(IllegalAction):
        pass

    def __init__(self, *, game):
        self._game = game

    def serialize(self):
        if self._game._collector:
            return {}

        if self._defender is None:
            return {}

        return self._legal_defenses

    def validate(self, player, base_card, card):
        if self._player(player) == self._game._durak:
            raise self.DefendingAsDurak
        if self._player(player) == self._game._collector:
            raise self.DefendingAfterGivingUp
        if self._player(player) != self._defender:
            raise self.DefendingOutOfTurn
        if card not in self._player(player).cards():
            raise self.DefendingWithOutOfHandCard
        self._validate_defense(base_card, card)

    def _validate_defense(self, base_card, card):
        try:
            if card not in self._legal_defenses[base_card]:
                raise self.InvalidDefense
        except KeyError:
            raise self.NoBaseCard

    @property
    def _legal_defenses(self):
        defender_cards = set(self._defender.cards())
        return {
            base_card: defender_cards & cards
            for base_card, cards in self._legal_defenses_for_table_cards.items()
        }

    @property
    def _legal_defenses_for_table_cards(self):
        return self._game._table.legal_defenses(trump_suit=self._game._trump_suit)

    @property
    def _defender(self):
        return self._game.defender

    def _player(self, player):
        return self._game.player(player)
