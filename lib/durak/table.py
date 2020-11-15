from itertools import chain
from operator import attrgetter

from lib.durak.card import get_all_cards, get_rank, is_legal_defense
from lib.durak.exceptions import IllegalAction


class Table:
    class TargetCardNotFound(IllegalAction):
        pass

    class DuplicateCard(IllegalAction):
        pass

    def __init__(self, *, game):
        self._game = game

    def serialize(self):
        return [attack.pair() for attack in self._sorted_attacks()]

    def attack(self, *, player, card):
        for table_card in self.cards():
            if table_card == card:
                raise self.DuplicateCard

        player.attack(card=card)

    def defend(self, *, player, attack_card, defense_card):
        for attack in self._sorted_attacks():
            if attack.attack != attack_card:
                continue

            attack.defend_with(card=player.remove_card(card=defense_card))
            return
        else:
            raise self.TargetCardNotFound

    def collect(self, *, player):
        player.take_cards(cards=self.cards())
        self._clear()

    def return_undefended(self):
        for player in self._game.ordered_players():
            player.take_cards(cards=self.undefended_cards())
            self._clear()

    def _clear(self):
        for player in self._game.ordered_players():
            player.attacks.clear()

    def legal_attacks(self):
        if not self._sorted_attacks():
            return set(get_all_cards())

        ranks_on_table = set(get_rank(card) for card in self.cards())
        return set(card for card in get_all_cards() if get_rank(card) in ranks_on_table)

    def legal_defenses(self, *, trump_suit):
        return {
            base_card: set(
                card
                for card in get_all_cards()
                if is_legal_defense(base_card, card, trump_suit)
            )
            for base_card in self.undefended_cards()
        }

    def legal_passes(self):
        if not self._sorted_attacks():
            return set([])
        # TODO: add a test for this clause
        if any(attack.defended() for attack in self._sorted_attacks()):
            return set([])

        ranks_on_table = set(get_rank(card) for card in self.cards())
        if len(ranks_on_table) > 1:
            return set([])

        return set(card for card in get_all_cards() if get_rank(card) in ranks_on_table)

    def undefended_cards(self):
        return [
            attack.attack for attack in self._sorted_attacks() if not attack.defended()
        ]

    def cards(self):
        return list(
            chain.from_iterable(attack.pair() for attack in self._sorted_attacks())
        )

    def _sorted_attacks(self):
        attacks = chain.from_iterable(
            player.attacks for player in self._game.ordered_players()
        )
        return sorted(list(attacks), key=attrgetter("timestamp"))
