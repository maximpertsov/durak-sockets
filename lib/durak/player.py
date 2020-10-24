from lib.durak.card import get_suit, get_value


class Player:
    HAND_SIZE = 6

    def __init__(self, *, name, order, cards, state=None):
        self.name = name
        self._cards = cards
        self.order = order
        self._state = set(state) if state else set()

    def serialize(self):
        return {
            "id": self.name,
            "hand": self._cards,
            "order": self.order,
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
    # Assuming that's true, you can remove the (100, ...) tuples.
    def organize_cards(self, *, strategy, trump_suit):
        if strategy == "group_by_rank":
            self._cards.sort(
                key=lambda card: (get_value(card), get_suit(card))
                if card
                else (100, 100)
            )
        elif strategy == "group_by_suit":
            self._cards.sort(
                key=lambda card: (get_suit(card), get_value(card))
                if card
                else (100, 100)
            )
        elif strategy == "group_by_rank_and_trump":
            self._cards.sort(
                key=lambda card: (
                    1 if get_suit(card) == trump_suit else 0,
                    get_value(card),
                    get_suit(card),
                )
                if card
                else (100, 100, 100)
            )

    def take_cards(self, *, cards):
        self._cards += cards

    def remove_card(self, *, card):
        self._cards = [
            None if hand_card == card else hand_card for hand_card in self._cards
        ]

    def draw(self, *, draw_pile):
        self.take_cards(cards=draw_pile.draw(count=self.draw_count()))

    def draw_count(self):
        return max(self.HAND_SIZE - self.card_count(), 0)

    def compact_hand(self):
        self._cards = self.cards()

    def had_cards_in_round(self):
        return bool(self._cards)

    def cards(self):
        return [card for card in self._cards if card]
