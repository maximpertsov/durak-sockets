from itertools import product

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


def key(rank, suit):
    short_rank = rank if rank == "10" else rank[0]
    short_suit = suit[0]

    return f"{short_rank}{short_suit}".upper()


DATA_BY_CARD = {
    key(rank, suit): {"rank": rank, "suit": suit}
    for rank, suit in product(RANKS, SUITS)
}


def get_rank(card):
    return DATA_BY_CARD[card]["rank"]

def get_suit(card):
    return DATA_BY_CARD[card]["suit"]
