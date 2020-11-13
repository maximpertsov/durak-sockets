from lib.durak.card import get_suit, get_value
from lib.durak.exceptions import IllegalAction
from lib.durak.status import Status


class Player:
    class BadOrganizationStrategy(IllegalAction):
        pass

    HAND_SIZE = 6

    @classmethod
    def deserialize(cls, player):
        return cls(
            id=player["id"],
            hand=player["hand"],
            order=player["order"],
            state=[Status(status) for status in player["state"]],
            organize_key=player.get("organize_strategy", "no_sort"),
        )

    def __init__(self, *, id, order, hand, organize_key, state):
        self.id = id
        self._hand = hand
        self.order = order
        self._state = set(state)
        self._organize_key = organize_key

    def serialize(self):
        return {
            "id": self.id,
            "hand": self._hand,
            "order": self.order,
            "state": self._state,
            "organize_strategy": self._organize_key,
        }

    def has_status(self, status):
        return status in self._state

    def add_status(self, status):
        self._state.add(status)

    def remove_status(self, status):
        self._state.discard(status)

    def card_count(self):
        return len(self.cards())

    def update_organize_strategy(self, *, strategy, trump_suit):
        if not self._organize_strategy_key(strategy, trump_suit):
            raise self.BadOrganizationStrategy

        self._organize_key = strategy

    def organize_cards(self, *, trump_suit):
        key = self._organize_strategy_key(self._organize_key, trump_suit)
        self._hand.sort(key=key)

    def _organize_strategy_key(self, strategy, trump_suit):
        if strategy == "no_sort":
            return lambda card: 0
        elif strategy == "group_by_rank":
            return lambda card: (get_value(card), get_suit(card))
        elif strategy == "group_by_suit":
            return lambda card: (get_suit(card), get_value(card))
        elif strategy == "group_by_rank_and_trump":
            return lambda card: (
                1 if get_suit(card) == trump_suit else 0,
                get_value(card),
                get_suit(card),
            )

    def take_cards(self, *, cards):
        self._hand += cards

    def remove_card(self, *, card):
        self._hand = [hand_card for hand_card in self._hand if hand_card != card]

    def draw(self, *, draw_pile):
        self.take_cards(cards=draw_pile.draw(count=self.draw_count()))

    def draw_count(self):
        return max(self.HAND_SIZE - self.card_count(), 0)

    def cards(self):
        return [card for card in self._hand if card]

    def remove_from_game(self):
        self.add_status(Status.OUT_OF_PLAY)
