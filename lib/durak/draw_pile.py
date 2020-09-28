from lib.durak.card import get_all_cards_shuffled, get_rank


class DrawPile:
    def __init__(self, *, drawn_cards, seed, lowest_rank):
        self._drawn_cards = set(drawn_cards)
        self._seed = seed
        self._lowest_rank = lowest_rank

    def serialize(self):
        return self._draw_pile

    def _draw_pile(self):
        return [
            card
            for card in get_all_cards_shuffled(self._seed)
            if self._is_drawable(card)
        ]

    def _is_drawable(self, card):
        if card in self._drawn_cards:
            return False
        if self._lowest_rank == "6" and get_rank(card) in "2345":
            return False
        return True

    def size(self):
        return len(self._draw_pile)

    def draw(self, count):
        drawn_cards = self._draw_pile[:count]
        self._drawn_cards.update(drawn_cards)
        return drawn_cards
