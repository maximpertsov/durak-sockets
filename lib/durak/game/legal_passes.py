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

        recipient_card_count = len(self._pass_recipient.cards())
        attack_limit = min(recipient_card_count, self._game._attack_limit)
        undefended_card_count = len(self._game._table.undefended_cards())

        return max(0, attack_limit - undefended_card_count)

    @property
    def _pass_recipient(self):
        if not self._defender:
            return

        players = self._game._ordered_players_with_cards_in_round()
        players_from_defender = players[2:] + [players[0]]
        next_players_with_cards = [
            player for player in players_from_defender if player.cards()
        ]
        if not next_players_with_cards:
            return
        return next_players_with_cards[0]

    @property
    def _defender(self):
        return self._game._defender()
