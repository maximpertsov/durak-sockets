from itertools import chain


class LegalAttacks:
    @classmethod
    def result(cls, *, game):
        return cls(game=game)._legal_attacks

    def __init__(self, *, game):
        self._game = game

    @property
    def _legal_attacks(self):
        return {
            "cards": self._cards,
            "limit": self._limit,
        }

    @property
    def _cards(self):
        if self._defender is None:
            return set()

        attackers = self._game._attackers()
        attacker_cards = chain.from_iterable(player.cards() for player in attackers)
        return set(attacker_cards) & self._game._table.legal_attacks()

    @property
    def _limit(self):
        if self._defender is None:
            return 0

        attack_limit = min(len(self._defender.cards()), self._game._attack_limit)
        undefended_cards = len(self._game._table.undefended_cards())
        return max(0, attack_limit - undefended_cards)

    @property
    def _defender(self):
        return self._game._defender()


class LegalDefenses:
    @classmethod
    def result(cls, *, game):
        return cls(game=game)._legal_defenses

    def __init__(self, *, game):
        self._game = game

    @property
    def _legal_defenses(self):
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

    @property
    def _defender(self):
        return self._game._defender()
