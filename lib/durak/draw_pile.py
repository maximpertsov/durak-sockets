from lib.durak.card import get_all_cards_shuffled, get_rank, get_suit


class DrawPile:
    def __init__(self, *, drawn_cards, seed, lowest_rank):
        self._drawn_cards = set(drawn_cards)
        self._seed = seed
        self._lowest_rank = lowest_rank

    def serialize(self):
        return {
            "cards_left": self.size(),
            "drawn_cards": self._drawn_cards,
            "lowest_rank": self._lowest_rank,
            "last_card": self.last_card,
            "seed": self._seed,
            "trump_suit": self.trump_suit,
        }

    def size(self):
        return len(self._draw_pile)

    def draw(self, count):
        drawn_cards = self._draw_pile[:count]
        self._drawn_cards.update(drawn_cards)
        return drawn_cards

    @property
    def trump_suit(self):
        return get_suit(self.last_card)

    @property
    def last_card(self):
        return [
            card
            for card in get_all_cards_shuffled(self._seed)
            if self._is_drawable_rank(card)
        ][-1]

    @property
    def _draw_pile(self):
        return [
            card
            for card in get_all_cards_shuffled(self._seed)
            if self._is_drawable(card)
        ]

    def _is_drawable(self, card):
        if card in self._drawn_cards:
            return False
        return self._is_drawable_rank(card)

    def _is_drawable_rank(self, card):
        if self._lowest_rank == "2":
            return True
        if self._lowest_rank == "6":
            return get_rank(card) not in "2345"

        raise ValueError(f"Invalid lowest rank {self._lowest_rank}")
