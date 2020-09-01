from itertools import chain

from lib.durak.card import get_all_cards, get_rank, is_legal_defense
from lib.durak.exceptions import IllegalAction


class Table:
    class BaseCardNotFound(IllegalAction):
        pass

    class DuplicateCard(IllegalAction):
        pass

    def __init__(self, table):
        self._table = table

    def serialize(self):
        return self._table

    def add_card(self, *, card):
        for table_card in self.cards():
            if table_card == card:
                raise self.DuplicateCard

        self._table.append([card])

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

    def undefended_cards(self):
        return [stack[0] for stack in self._table if len(stack) == 1]

    def stack_card(self, *, base_card, card):
        for cards in self._table:
            if cards[-1] == base_card:
                cards.append(card)
                return
        else:
            raise self.BaseCardNotFound

    def clear(self):
        self._table.clear()

    def collect(self):
        result = self.cards()
        self.clear()
        return result

    def cards(self):
        return list(chain.from_iterable(self._table))
