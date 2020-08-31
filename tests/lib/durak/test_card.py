import pytest

from lib.durak.card import get_rank, get_suit, is_legal_defense


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


@pytest.mark.parametrize(
    "attack_card,defense_card,trump_suit,expected",
    [
        ("6H", "7H", "spades", True),
        ("7H", "6H", "spades", False),
        ("6H", "7C", "spades", False),
        ("AH", "7S", "spades", True),
    ],
)
def test_is_legal_defense(attack_card, defense_card, trump_suit, expected):
    assert is_legal_defense(attack_card, defense_card, trump_suit) == expected
