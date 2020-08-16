import pytest
from lib.durak import Table


@pytest.fixture
def table():
    return [
        [{"rank": "8", "suit": "diamonds"}, {"rank": "10", "suit": "diamonds"}],
        [{"rank": "10", "suit": "clubs"}],
    ]


def test_add_card(table):
    subject = Table(table=table)
    subject.add_card(card={"rank": "jack", "suit": "clubs"},)
    assert subject.serialize() == [
        [{"rank": "8", "suit": "diamonds"}, {"rank": "10", "suit": "diamonds"}],
        [{"rank": "10", "suit": "clubs"}],
        [{"rank": "jack", "suit": "clubs"}],
    ]


def test_stack_card(table):
    subject = Table(table=table)
    subject.stack_card(
        base_card={"rank": "10", "suit": "clubs"},
        card={"rank": "jack", "suit": "clubs"},
    )
    assert subject.serialize() == [
        [{"rank": "8", "suit": "diamonds"}, {"rank": "10", "suit": "diamonds"}],
        [{"rank": "10", "suit": "clubs"}, {"rank": "jack", "suit": "clubs"}],
    ]


def test_stack_card_on_nonexistent_base_card(table):
    subject = Table(table=table)

    with pytest.raises(Table.BaseCardNotFound):
        subject.stack_card(
            base_card={"rank": "8", "suit": "diamonds"},
            card={"rank": "jack", "suit": "clubs"},
        )
