from collections import deque
from itertools import groupby

from lib.durak.card import get_value
from lib.durak.exceptions import IllegalAction


class LegalPasses:
    class PassingAsDurak(IllegalAction):
        pass

    class PassingWithOutOfHandCard(IllegalAction):
        pass

    class PassingWithTooManyCards(IllegalAction):
        pass

    class PassingOutOfTurn(IllegalAction):
        pass

    class EmptyPass(IllegalAction):
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
            raise self.EmptyPass
        if self._game._durak == self._player(player):
            raise self.PassingAsDurak
        if self._player(player) != self._defender:
            raise self.PassingOutOfTurn
        if not set(cards) <= set(self._player(player).cards()):
            raise self.PassingWithOutOfHandCard
        if len(cards) > self._limit:
            raise self.PassingWithTooManyCards
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
        if self._pass_recipient is None:
            return set()

        return set(self._defender.cards()) & self._game._table.legal_passes()

    @property
    def _groups(self):
        if not self._cards:
            return []

        cards = sorted(self._cards, key=get_value)
        return [set(group) for _, group in groupby(cards, get_value)]

    @property
    def _limit(self):
        if self._pass_recipient is None:
            return 0

        undefended_card_count = len(self._game._table.undefended_cards())
        return max(0, self._attack_limit - undefended_card_count)

    @property
    def _attack_limit(self):
        if self._game._attack_limit == "six":
            return min(6, self._pass_recipient.card_count())
        if self._game._attack_limit == "hand":
            return self._pass_recipient.card_count()
        if self._game._attack_limit == "unlimited":
            return 100

        raise self.InvalidAttackLimit

    @property
    def _pass_recipient(self):
        if not self._defender:
            return

        players = deque(self._game.ordered_players_in_play())
        players.rotate(2)
        try:
            return next(
                player
                for player in players
                if player.cards() and self._player(player) != self._defender
            )
        except StopIteration:
            return

    @property
    def _defender(self):
        return self._game.defender

    def _player(self, player):
        return self._game.player(player)
