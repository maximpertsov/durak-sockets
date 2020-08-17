import pytest
from lib.durak import DrawPile, Player


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
        order=0,
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
        "order": 0,
        "yielded": False,
    }


def test_card_count(player):
    assert player.card_count() == 6


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
        "order": 0,
        "yielded": False,
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
        "order": 0,
        "yielded": False,
    }


def test_draw_from_pile():
    player = Player(
        name="anna",
        cards=[
            {"rank": "10", "suit": "diamonds"},
            None,
            {"rank": "10", "suit": "clubs"},
        ],
        order=0,
    )
    draw_pile = DrawPile(
        draw_pile=[
            {"rank": "2", "suit": "spades"},
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
            {"rank": "ace", "suit": "spades"},
        ]
    )
    player.draw(draw_pile=draw_pile)
    assert player.serialize() == {
        "name": "anna",
        "cards": [
            {"rank": "10", "suit": "diamonds"},
            {"rank": "10", "suit": "clubs"},
            {"rank": "2", "suit": "spades"},
            {"rank": "5", "suit": "clubs"},
            {"rank": "8", "suit": "diamonds"},
            {"rank": "2", "suit": "clubs"},
        ],
        "order": 0,
        "yielded": False,
    }
    assert draw_pile.serialize() == [
        {"rank": "ace", "suit": "spades"},
    ]
