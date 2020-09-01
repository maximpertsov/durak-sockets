import pytest

from lib.durak.card import get_cards_of_suit
from lib.durak.table import Table


@pytest.fixture
def table():
    return Table(table=[["8D", "10D"], ["10C"]])


def test_add_card(table):
    table.add_card(card="JC")
    assert table.serialize() == [
        ["8D", "10D"],
        ["10C"],
        ["JC"],
    ]


def test_stack_card(table):
    table.stack_card(
        base_card="10C", card="JC",
    )
    assert table.serialize() == [
        ["8D", "10D"],
        ["10C", "JC"],
    ]


def test_stack_card_on_nonexistent_base_card(table):
    with pytest.raises(Table.BaseCardNotFound):
        table.stack_card(
            base_card="8D", card="JC",
        )


def test_clear(table):
    table.clear()
    assert table.serialize() == []


def test_collect(table):
    assert table.collect() == [
        "8D",
        "10D",
        "10C",
    ]
    assert table.serialize() == []


def test_duplicate_card(table):
    with pytest.raises(Table.DuplicateCard):
        table.add_card(card="10C")


def test_legal_defenses(table):
    table.add_card(card="JD")
    trump_suit = "diamonds"
    diamonds = get_cards_of_suit(trump_suit)
    assert table.legal_defenses(trump_suit=trump_suit) == {
        "JD": set(["QD", "KD", "AD"]),
        "10C": set(diamonds + ["JC", "QC", "KC", "AC"]),
    }


def test_legal_attacks(table):
    assert table.legal_attacks() == set(
        ["10H", "10D", "10C", "10S", "8H", "8D", "8C", "8S"]
    )
