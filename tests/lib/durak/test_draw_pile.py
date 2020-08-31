import pytest

from lib.durak import DrawPile


@pytest.fixture
def draw_pile():
    return ["10D", "10C", "2S", "5C", "8D", "2C"]


def test_draw_pile_size(draw_pile):
    subject = DrawPile(draw_pile=draw_pile)
    assert subject.size() == 6


def test_draw_from_pile(draw_pile):
    subject = DrawPile(draw_pile=draw_pile)
    assert subject.draw(count=2) == ["10D", "10C"]
    assert subject.serialize() == ["2S", "5C", "8D", "2C"]
