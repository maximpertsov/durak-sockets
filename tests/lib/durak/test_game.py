import pytest
from lib.durak import Game


@pytest.fixture
def game():
    return Game(
        draw_pile=[
            {"rank": "jack", "suit": "clubs"},
            {"rank": "3", "suit": "spades"},
            {"rank": "6", "suit": "clubs"},
        ],
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
        },
        players=["anna"],
        table=[],
        yielded=[],
    )


def test_serialize(game):
    assert game.serialize() == {
        "draw_pile": [
            {"rank": "jack", "suit": "clubs"},
            {"rank": "3", "suit": "spades"},
            {"rank": "6", "suit": "clubs"},
        ],
        "hands": {
            "anna": [
                {"rank": "10", "suit": "diamonds"},
                None,
                {"rank": "10", "suit": "clubs"},
                {"rank": "2", "suit": "spades"},
                {"rank": "5", "suit": "clubs"},
                {"rank": "8", "suit": "diamonds"},
                {"rank": "2", "suit": "clubs"},
            ]
        },
        "players": ["anna"],
        "table": [],
        "yielded": [],
    }
