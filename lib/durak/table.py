from itertools import chain

from lib.durak.card import get_all_cards, is_legal_defense
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
        for table_card in self._all_cards():
            if table_card == card:
                raise self.DuplicateCard

        self._table.append([card])

    def valid_defenses(self, *, trump_suit):
        return {
            base_card: set(
                card
                for card in get_all_cards()
                if is_legal_defense(base_card, card, trump_suit)
            )
            for base_card in self._undefended_cards()
        }

    def _undefended_cards(self):
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
        result = self._all_cards()
        self.clear()
        return result

    def _all_cards(self):
        return list(chain.from_iterable(self._table))
