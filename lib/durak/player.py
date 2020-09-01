class Player:
    HAND_SIZE = 6

    def __init__(self, *, name, cards, order, yielded=False):
        self.name = name
        self._cards = cards
        self.order = order
        self.yielded = yielded

    def serialize(self):
        return {
            "name": self.name,
            "cards": self._cards,
            "order": self.order,
            "yielded": self.yielded,
        }

    def card_count(self):
        return sum(1 for card in self._cards if card)

    def in_game(self):
        return bool(self._cards)

    def take_cards(self, *, cards):
        # TODO: maybe compacting should happen client-side?
        self._compact_hand()
        self._cards += cards

    def remove_card(self, *, card):
        self._cards = [
            None if hand_card == card else hand_card for hand_card in self._cards
        ]

    def draw(self, *, draw_pile):
        draw_count = max(self.HAND_SIZE - self.card_count(), 0)
        self.take_cards(cards=draw_pile.draw(count=draw_count))
        # TODO: maybe compacting should happen client-side?
        self._compact_hand()

    def _compact_hand(self):
        self._cards = self.cards()

    def cards(self):
        return [card for card in self._cards if card]
