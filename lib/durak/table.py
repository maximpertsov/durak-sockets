from itertools import chain

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
