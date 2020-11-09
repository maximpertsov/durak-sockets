from lib.durak.card import get_suit, get_value
from lib.durak.status import Status


class Player:
    HAND_SIZE = 6

    @classmethod
    def deserialize(cls, player):
        return cls(
            id=player["id"],
            hand=player["hand"],
            order=player["order"],
            state=[Status(status) for status in player["state"]],
        )

    def __init__(self, *, id, order, hand, state=None):
        self.id = id
        self._hand = hand
        self.order = order
        self._state = set(state) if state else set()

    def serialize(self):
        return {
            "id": self.id,
            "hand": self._hand,
            "order": self.order,
            "state": self._state,
        }

    def has_status(self, status):
        return status in self._state

    def add_status(self, status):
        self._state.add(status)

    def remove_status(self, status):
        self._state.discard(status)

    def card_count(self):
        return len(self.cards())

    # TODO: ensure that null cards are not required for game logic.
    # Assuming that's true, you can remove the (100, "z", ...) tuples.
    def organize_cards(self, *, strategy, trump_suit):
        print(self._hand)
        if strategy == "group_by_rank":
            self._hand.sort(
                key=lambda card: (get_value(card), get_suit(card))
                if card
                else (100, "z")
            )
        elif strategy == "group_by_suit":
            self._hand.sort(
                key=lambda card: (get_suit(card), get_value(card))
                if card
                else ("z", 100)
            )
        elif strategy == "group_by_rank_and_trump":
            self._hand.sort(
                key=lambda card: (
                    1 if get_suit(card) == trump_suit else 0,
                    get_value(card),
                    get_suit(card),
                )
                if card
                else (100, 100, "z")
            )

    def take_cards(self, *, cards):
        self._hand += cards

    def remove_card(self, *, card):
        self._hand = [
            None if hand_card == card else hand_card for hand_card in self._hand
        ]

    def draw(self, *, draw_pile):
        self.take_cards(cards=draw_pile.draw(count=self.draw_count()))

    def draw_count(self):
        return max(self.HAND_SIZE - self.card_count(), 0)

    def compact_hand(self):
        self._hand = self.cards()

    def had_cards_in_round(self):
        return bool(self._hand)

    def cards(self):
        return [card for card in self._hand if card]

    def remove_from_game(self):
        self.add_status(Status.OUT_OF_PLAY)
