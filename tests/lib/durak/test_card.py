import pytest

from lib.durak.card import get_all_cards_shuffled, get_rank, get_suit, is_legal_defense


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


def test_get_all_cards_shuffled():
    cards = get_all_cards_shuffled(seed=0.4)
    assert cards == [
        "7H",
        "6H",
        "KH",
        "QD",
        "6D",
        "KD",
        "9H",
        "7S",
        "AD",
        "5C",
        "10C",
        "KC",
        "9S",
        "JH",
        "5H",
        "8S",
        "3C",
        "3H",
        "3D",
        "6C",
        "QH",
        "QC",
        "8D",
        "QS",
        "4C",
        "9C",
        "AC",
        "9D",
        "5D",
        "AH",
        "AS",
        "8C",
        "JS",
        "7C",
        "5S",
        "6S",
        "2C",
        "10D",
        "KS",
        "2D",
        "8H",
        "3S",
        "JC",
        "10S",
        "2H",
        "4S",
        "4D",
        "7D",
        "JD",
        "2S",
        "10H",
        "4H",
    ]
