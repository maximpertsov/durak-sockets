import pytest

from lib.durak import Game


@pytest.fixture
def game():
    return Game.deserialize(
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
        pass_count=0,
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
        "pass_count": 0,
        "players": ["anna"],
        "table": [],
        "yielded": [],
    }


def test_attack(game):
    game.attack(player="anna", card={"rank": "10", "suit": "diamonds"})
    assert game.serialize() == {
        "draw_pile": [
            {"rank": "jack", "suit": "clubs"},
            {"rank": "3", "suit": "spades"},
            {"rank": "6", "suit": "clubs"},
        ],
        "hands": {
            "anna": [
                None,
                None,
                {"rank": "10", "suit": "clubs"},
                {"rank": "2", "suit": "spades"},
                {"rank": "5", "suit": "clubs"},
                {"rank": "8", "suit": "diamonds"},
                {"rank": "2", "suit": "clubs"},
            ]
        },
        "pass_count": 0,
        "players": ["anna"],
        "table": [[{"rank": "10", "suit": "diamonds"}]],
        "yielded": [],
    }


def test_defend(game):
    nine_of_diamonds = {"rank": "9", "suit": "diamonds"}
    game._table.add_card(card=nine_of_diamonds)
    game.defend(
        base_card=nine_of_diamonds,
        player="anna",
        card={"rank": "10", "suit": "diamonds"},
    )
    assert game.serialize() == {
        "draw_pile": [
            {"rank": "jack", "suit": "clubs"},
            {"rank": "3", "suit": "spades"},
            {"rank": "6", "suit": "clubs"},
        ],
        "hands": {
            "anna": [
                None,
                None,
                {"rank": "10", "suit": "clubs"},
                {"rank": "2", "suit": "spades"},
                {"rank": "5", "suit": "clubs"},
                {"rank": "8", "suit": "diamonds"},
                {"rank": "2", "suit": "clubs"},
            ]
        },
        "pass_count": 0,
        "players": ["anna"],
        "table": [[nine_of_diamonds, {"rank": "10", "suit": "diamonds"}]],
        "yielded": [],
    }


def test_draw(game):
    pass
