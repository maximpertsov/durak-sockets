from itertools import chain, groupby

from lib.durak.card import get_value
from lib.durak.exceptions import IllegalAction


class LegalAttacks:
    class AttackingAsDurak(IllegalAction):
        pass

    class AttackingWithOutOfHandCard(IllegalAction):
        pass

    class AttackingWithTooManyCards(IllegalAction):
        pass

    class AttackingOutOfTurn(IllegalAction):
        pass

    class EmptyAttack(IllegalAction):
        pass

    class IllegalCard(IllegalAction):
        pass

    class IllegalGrouping(IllegalAction):
        pass

    class InvalidAttackLimit(IllegalAction):
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
        if not cards:
            raise self.EmptyAttack
        if self._game._durak == self._player(player):
            raise self.AttackingAsDurak
        if self._player(player) not in self._attackers:
            raise self.AttackingOutOfTurn
        if not set(cards) <= set(self._player(player).cards()):
            raise self.AttackingWithOutOfHandCard
        if len(cards) > self._limit:
            raise self.AttackingWithTooManyCards
        # TODO: is this duplicated the next check?
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

        attacker_cards = chain.from_iterable(
            player.cards() for player in self._attackers
        )
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

        undefended_cards = len(self._game._table.undefended_cards())
        return max(0, self._attack_limit - undefended_cards)

    @property
    def _attack_limit(self):
        if self._game._attack_limit == "six":
            return min(6, self._defender.card_count())
        if self._game._attack_limit == "hand":
            return self._defender.card_count()
        if self._game._attack_limit == "unlimited":
            return self._defender.card_count() if self._game.collector else 100

        raise self.InvalidAttackLimit

    @property
    def _attackers(self):
        return self._game.attackers

    @property
    def _defender(self):
        return self._game.defender

    def _player(self, player):
        return self._game.player(player)
