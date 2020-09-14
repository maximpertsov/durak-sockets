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
        return len(self.cards())

    def organize_cards(self, *, strategy, trump_suit):
        self._compact_hand()
        if strategy == 'group_by_rank':
            return
        elif strategy == 'group_by_suit':
            return
        elif strategy == 'group_by_rank_and_trumps':
            return

    def take_cards(self, *, cards):
        self._compact_hand()
        self._cards += cards

    def remove_card(self, *, card):
        self._cards = [
            None if hand_card == card else hand_card for hand_card in self._cards
        ]

    def draw(self, *, draw_pile):
        draw_count = max(self.HAND_SIZE - self.card_count(), 0)
        self.take_cards(cards=draw_pile.draw(count=draw_count))
        self._compact_hand()

    def _compact_hand(self):
        self._cards = self.cards()

    def had_cards_in_round(self):
        return bool(self._cards)

    def cards(self):
        return [card for card in self._cards if card]
