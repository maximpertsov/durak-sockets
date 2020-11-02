from itertools import chain, groupby

from lib.durak.card import get_value
from lib.durak.exceptions import IllegalAction


class LegalAttacks:
    class AttackingWithTooManyCards(IllegalAction):
        pass

    class AttackingOutOfTurn(IllegalAction):
        pass

    class IllegalCard(IllegalAction):
        pass

    class IllegalGrouping(IllegalAction):
        pass

    def __init__(self, *, game):
        self._game = game

    def serialize(self):
        return {
            "cards": self._cards,
            # "groups": self._groups,
            "limit": self._limit,
        }

    def validate(self, player, cards):
        if self._player(player) not in self._attackers:
            raise self.AttackingOutOfTurn
        if len(cards) > self._limit:
            raise self.AttackingWithTooManyCards
        # TODO: is this duplicated by the next check?
        self._validate_cards(cards)
        self._validate_group(cards)

    def _validate_cards(self, cards):
        legal_cards = self._cards
        for card in cards:
            if card not in legal_cards:
                raise self.IllegalCard(card)

    def _validate_group(self, cards):
        for group in self._groups:
            if set(cards).issubset(group):
                break
        else:
            raise self.IllegalGrouping

    @property
    def _cards(self):
        if self._defender is None:
            return set()

        attackers = self._game._attackers()
        attacker_cards = chain.from_iterable(player.cards() for player in attackers)
        return set(attacker_cards) & self._game._table.legal_attacks()

    @property
    def _groups(self):
        if not self._cards:
            return []

        if self._game._table.cards():
            return [set(self._cards)]

        cards = sorted(self._cards, key=get_value)
        return [set(group) for _, group in groupby(cards, get_value)]

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

    @property
    def _attackers(self):
        return self._game._attackers()

    def _player(self, player):
        return self._game.player(player)