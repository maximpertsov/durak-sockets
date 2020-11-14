from itertools import chain
from typing import List, Optional

from lib.durak.card import get_all_cards, get_rank, is_legal_defense
from lib.durak.exceptions import IllegalAction
from lib.durak.player import Player


class TableItem:
    def __init__(
        self,
        *,
        player: Optional[Player] = None,
        attack: str,
        defense: Optional[str] = None
    ) -> None:
        self.player = player
        self.attack = attack
        self.defense = defense

    def serialize(self):
        # TODO: temporary signature
        return self.cards()

        # return {
        #     "player": self.player.id if self.player else None,
        #     "attack": self.attack,
        #     "defense": self.defense,
        # }

    def defended(self):
        return self.defense is None

    def cards(self):
        return list(filter(None, [self.attack, self.defense]))


class Table:
    class BaseCardNotFound(IllegalAction):
        pass

    class DuplicateCard(IllegalAction):
        pass

    @classmethod
    def deserialize(cls, table):
        # TODO: temporary signature
        return cls(
            [
                TableItem(
                    player=None, attack=attack, defense=cards[0] if cards else None
                )
                for attack, *cards in table
            ]
        )

    def __init__(self, table):
        self._table = table

    def serialize(self):
        return [item.serialize() for item in self._table]

    def add_card(self, *, card: str) -> None:
        for table_card in self.cards():
            if table_card == card:
                raise self.DuplicateCard

        self._table.append(TableItem(player=None, attack=card, defense=None))

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

    def undefended_cards(self) -> List[TableItem]:
        return [item.attack for item in self._table if not item.defended()]

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
        return list(chain.from_iterable(item.cards() for item in self._table))
