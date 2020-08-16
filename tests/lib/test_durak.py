import pytest

from lib.durak import Hands


@pytest.fixture
def hands():
    return {
        "anna": [
            {"rank": "10", "suit": "diamonds"},
            {"rank": "10", "suit": "clubs"},
            {"rank": "2", "suit": "spades"},
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
        ],
    }


def test_remove_card_from_anna(hands):
    subject = Hands(hands=hands)
    assert subject.serialize() == {
        "anna": [
            {"rank": "10", "suit": "diamonds"},
            {"rank": "10", "suit": "clubs"},
            {"rank": "2", "suit": "spades"},
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
        ]
    }
    subject.remove_card(player="anna", card={"rank": "2", "suit": "spades"})
    assert subject.serialize() == {
        "anna": [
            {"rank": "10", "suit": "diamonds"},
            {"rank": "10", "suit": "clubs"},
            None,
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
        ]
    }
