import pytest
from lib.durak import Player


@pytest.fixture
def player():
    return Player(
        name="anna",
        cards=[
            {"rank": "10", "suit": "diamonds"},
            None,
            {"rank": "10", "suit": "clubs"},
            {"rank": "2", "suit": "spades"},
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
        ],
    )


def test_serialize(player):
    assert player.serialize() == {
        "name": "anna",
        "cards": [
            {"rank": "10", "suit": "diamonds"},
            None,
            {"rank": "10", "suit": "clubs"},
            {"rank": "2", "suit": "spades"},
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
        ],
    }


def test_take_cards(player):
    player.take_cards(
        cards=[{"rank": "3", "suit": "spades"}, {"rank": "4", "suit": "diamonds"}],
    )
    assert player.serialize() == {
        "name": "anna",
        "cards": [
            {"rank": "10", "suit": "diamonds"},
            {"rank": "10", "suit": "clubs"},
            {"rank": "2", "suit": "spades"},
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
            {"rank": "3", "suit": "spades"},
            {"rank": "4", "suit": "diamonds"},
        ],
    }


def test_remove_card(player):
    player.remove_card(card={"rank": "2", "suit": "spades"})
    assert player.serialize() == {
        "name": "anna",
        "cards": [
            {"rank": "10", "suit": "diamonds"},
            None,
            {"rank": "10", "suit": "clubs"},
            None,
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
        ],
    }
