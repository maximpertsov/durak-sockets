from itertools import product
from random import Random

SUITS = ["clubs", "diamonds", "hearts", "spades"]
RANKS = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "jack",
    "queen",
    "king",
    "ace",
]


def _key(rank, suit):
    short_rank = rank if rank == "10" else rank[0]
    short_suit = suit[0]

    return f"{short_rank}{short_suit}".upper()


_DATA_BY_CARD = {
    _key(rank, suit): {
        "sort_key": sort_key,
        "rank": rank,
        "suit": suit,
        "value": rank_value,
    }
    for sort_key, ((rank_value, rank), suit) in enumerate(
        product(enumerate(RANKS), SUITS)
    )
}


def get_all_cards():
    return list(_DATA_BY_CARD)


def get_all_cards_shuffled(seed):
    cards = get_all_cards()
    cards.sort(key=lambda card: _DATA_BY_CARD[card]["sort_key"])
    Random(seed).shuffle(cards)
    return cards


def get_rank(card):
    return _DATA_BY_CARD[card]["rank"]


def get_suit(card):
    return _DATA_BY_CARD[card]["suit"]


def get_value(card):
    return _DATA_BY_CARD[card]["value"]


def get_cards_of_suit(suit):
    return [card for card, data in _DATA_BY_CARD.items() if data["suit"] == suit]


def is_legal_defense(attack_card, defense_card, trump_suit):
    if get_suit(attack_card) == get_suit(defense_card):
        return get_value(defense_card) > get_value(attack_card)
    return get_suit(defense_card) == trump_suit
