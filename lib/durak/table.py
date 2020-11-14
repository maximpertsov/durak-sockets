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

    def defend(self, *, attack_card, defense_card):
        for attack in self._sorted_attacks():
            if attack.attack != attack_card:
                continue

            attack.defend_with(card=defense_card)
            return
        else:
            raise self.TargetCardNotFound

    def legal_defenses(self, *, trump_suit):
        return {
            base_card: set(
                card
                for card in get_all_cards()
                if is_legal_defense(base_card, card, trump_suit)
            )
            for base_card in self.undefended_cards()
        }

    def legal_attacks(self):
        if not self._table:
            return set(get_all_cards())

        ranks_on_table = set(get_rank(card) for card in self.cards())
        return set(card for card in get_all_cards() if get_rank(card) in ranks_on_table)

    def legal_passes(self):
        if not self._table:
            return set([])
        if any(len(stack) > 1 for stack in self._table):
            return set([])

        ranks_on_table = set(get_rank(card) for card in self.cards())
        if len(ranks_on_table) > 1:
            return set([])

        return set(card for card in get_all_cards() if get_rank(card) in ranks_on_table)

    def undefended_cards(self):
        return [stack[0] for stack in self._table if len(stack) == 1]

    def clear(self):
        self._table.clear()

    def collect(self):
        result = self.cards()
        self.clear()
        return result

    def cards(self):
        return list(
            chain.from_iterable(attack.pair() for attack in self._sorted_attacks())
        )

    def _sorted_attacks(self):
        attacks = chain.from_iterable(
            player.attacks for player in self._game.ordered_players()
        )
        return sorted(list(attacks), key=attrgetter("timestamp"))
