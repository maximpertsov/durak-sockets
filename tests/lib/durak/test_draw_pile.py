import pytest
from lib.durak import DrawPile


@pytest.fixture
def draw_pile():
    return [
        {"rank": "10", "suit": "diamonds"},
        {"rank": "10", "suit": "clubs"},
        {"rank": "2", "suit": "spades"},
        {"rank": "5", "suit": "clubs"},
        {"rank": "8", "suit": "diamonds"},
        {"rank": "2", "suit": "clubs"},
    ]


def test_draw_pile_size(draw_pile):
    subject = DrawPile(draw_pile=draw_pile)
    assert subject.size() == 6


def test_draw_from_pile(draw_pile):
    subject = DrawPile(draw_pile=draw_pile)
    assert subject.draw(count=2) == [
        {"rank": "10", "suit": "diamonds"},
        {"rank": "10", "suit": "clubs"},
    ]
    assert subject.serialize() == [
        {"rank": "2", "suit": "spades"},
        {"rank": "5", "suit": "clubs"},
        {"rank": "8", "suit": "diamonds"},
        {"rank": "2", "suit": "clubs"},
    ]
