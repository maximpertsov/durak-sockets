import pytest
from lib.durak import Hands


@pytest.fixture
def hands():
    return Hands(
        hands={
            "anna": [
                {"rank": "10", "suit": "diamonds"},
                None,
                {"rank": "10", "suit": "clubs"},
                {"rank": "2", "suit": "spades"},
                {"rank": "5", "suit": "clubs"},
                {"rank": "8", "suit": "diamonds"},
                {"rank": "2", "suit": "clubs"},
            ],
        }
    )


def test_serialize(hands):
    assert hands.serialize() == {
        "anna": [
            {"rank": "10", "suit": "diamonds"},
            None,
            {"rank": "10", "suit": "clubs"},
            {"rank": "2", "suit": "spades"},
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
        ]
    }


def test_take_cards(hands):
    hands.take_cards(
        player="anna",
        cards=[{"rank": "3", "suit": "spades"}, {"rank": "4", "suit": "diamonds"}],
    )
    assert hands.serialize() == {
        "anna": [
            {"rank": "10", "suit": "diamonds"},
            {"rank": "10", "suit": "clubs"},
            {"rank": "2", "suit": "spades"},
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
            {"rank": "3", "suit": "spades"},
            {"rank": "4", "suit": "diamonds"},
        ]
    }


def test_remove_card(hands):
    hands.remove_card(player="anna", card={"rank": "2", "suit": "spades"})
    assert hands.serialize() == {
        "anna": [
            {"rank": "10", "suit": "diamonds"},
            None,
            {"rank": "10", "suit": "clubs"},
            None,
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
        ]
    }
