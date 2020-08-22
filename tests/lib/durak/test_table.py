import pytest

from lib.durak import BaseCardNotFound, DuplicateCard, Table


@pytest.fixture
def table():
    return Table(
        table=[
            [{"rank": "8", "suit": "diamonds"}, {"rank": "10", "suit": "diamonds"}],
            [{"rank": "10", "suit": "clubs"}],
        ]
    )


def test_add_card(table):
    table.add_card(card={"rank": "jack", "suit": "clubs"},)
    assert table.serialize() == [
        [{"rank": "8", "suit": "diamonds"}, {"rank": "10", "suit": "diamonds"}],
        [{"rank": "10", "suit": "clubs"}],
        [{"rank": "jack", "suit": "clubs"}],
    ]


def test_stack_card(table):
    table.stack_card(
        base_card={"rank": "10", "suit": "clubs"},
        card={"rank": "jack", "suit": "clubs"},
    )
    assert table.serialize() == [
        [{"rank": "8", "suit": "diamonds"}, {"rank": "10", "suit": "diamonds"}],
        [{"rank": "10", "suit": "clubs"}, {"rank": "jack", "suit": "clubs"}],
    ]


def test_stack_card_on_nonexistent_base_card(table):
    with pytest.raises(BaseCardNotFound):
        table.stack_card(
            base_card={"rank": "8", "suit": "diamonds"},
            card={"rank": "jack", "suit": "clubs"},
        )


def test_clear(table):
    table.clear()
    assert table.serialize() == []


def test_collect(table):
    assert table.collect() == [
        {"rank": "8", "suit": "diamonds"},
        {"rank": "10", "suit": "diamonds"},
        {"rank": "10", "suit": "clubs"},
    ]
    assert table.serialize() == []


def test_duplicate_card(table):
    with pytest.raises(DuplicateCard):
        table.add_card(card={"rank": "10", "suit": "clubs"})
