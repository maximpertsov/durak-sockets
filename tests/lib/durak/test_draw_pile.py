import pytest

from lib.durak.draw_pile import DrawPile


@pytest.fixture
def cards():
    return ["10D", "10C", "2S", "5C", "8D", "2C"]


@pytest.fixture
def mocked_draw_cards(cards, get_draw_pile_cards):
    return get_draw_pile_cards(cards)


@pytest.fixture
def default_parameters():
    return {
        "drawn_cards": [],
        "seed": 0.4,
        "lowest_rank": "2",
    }


def test_draw_pile_size(default_parameters, mocked_draw_cards):
    subject = DrawPile(**default_parameters)
    assert subject.serialize() == {
        **default_parameters,
        "drawn_cards": set(),
        "cards_left": 6,
        "last_card": "2C",
        "trump_suit": "clubs",
    }
    mocked_draw_cards.assert_called_with(default_parameters["seed"])


def test_drawn_cards(default_parameters, mocked_draw_cards):
    args = {**default_parameters, "drawn_cards": ["10D", "10C"]}
    subject = DrawPile(**args)
    assert subject.serialize() == {
        **default_parameters,
        "drawn_cards": set(["10D", "10C"]),
        "cards_left": 4,
        "last_card": "2C",
        "trump_suit": "clubs",
    }
    mocked_draw_cards.assert_called_with(default_parameters["seed"])


def test_lowest_rank_is_six(default_parameters, mocked_draw_cards):
    args = {**default_parameters, "lowest_rank": "6"}
    subject = DrawPile(**args)
    assert subject.serialize() == {
        **default_parameters,
        "drawn_cards": set(),
        "cards_left": 3,
        "last_card": "8D",
        "lowest_rank": "6",
        "trump_suit": "diamonds",
    }
    mocked_draw_cards.assert_called_with(default_parameters["seed"])


def test_draw_from_pile(default_parameters, mocked_draw_cards):
    subject = DrawPile(**default_parameters)
    assert subject.draw(count=2) == ["10D", "10C"]
    assert subject.serialize() == {
        **default_parameters,
        "drawn_cards": set(["10D", "10C"]),
        "cards_left": 4,
        "last_card": "2C",
        "trump_suit": "clubs",
    }
    mocked_draw_cards.assert_called_with(default_parameters["seed"])
