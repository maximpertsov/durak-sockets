from itertools import groupby

from lib.durak.card import get_value


class Base:
    @classmethod
    def result(cls, *, game):
        return cls(game=game)._result

    def __init__(self, *, game):
        self._game = game

    @property
    def _result(self):
        raise NotImplementedError

    @property
    def _defender(self):
        return self._game._defender()


class LegalDefenses(Base):
    @property
    def _result(self):
        if self._game._collector:
            return {}

        if self._defender is None:
            return {}

        defender_cards = set(self._defender.cards())
        return {
            base_card: defender_cards & cards
            for base_card, cards in self._legal_defenses_for_table_cards.items()
        }

    @property
    def _legal_defenses_for_table_cards(self):
        return self._game._table.legal_defenses(trump_suit=self._game._trump_suit)
