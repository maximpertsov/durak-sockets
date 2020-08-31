import pytest

from lib.durak.card import get_rank, get_suit


@pytest.mark.parametrize(
    "card,rank,suit",
    [
        ("6H", "6", "hearts"),
        ("7H", "7", "hearts"),
        ("AH", "ace", "hearts"),
        ("7C", "7", "clubs"),
        ("10S", "10", "spades"),
        ("QD", "queen", "diamonds"),
    ],
)
def test_get_rank_and_suit(card, rank, suit):
    assert get_rank(card) == rank
    assert get_suit(card) == suit
