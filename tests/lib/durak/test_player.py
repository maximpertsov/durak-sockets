import pytest

from lib.durak.draw_pile import DrawPile
from lib.durak.player import Player


@pytest.fixture
def player():
    return Player(
        name="anna", cards=["10D", None, "10C", "2S", "5C", "8D", "2C"], order=0,
    )


def test_serialize(player):
    assert player.serialize() == {
        "name": "anna",
        "cards": ["10D", None, "10C", "2S", "5C", "8D", "2C"],
        "order": 0,
        "yielded": False,
    }


def test_card_count(player):
    assert player.card_count() == 6


def test_take_cards(player):
    player.take_cards(cards=["3S", "4D"])
    assert player.serialize() == {
        "name": "anna",
        "cards": ["10D", "10C", "2S", "5C", "8D", "2C", "3S", "4D"],
        "order": 0,
        "yielded": False,
    }


def test_remove_card(player):
    player.remove_card(card="2S")
    assert player.serialize() == {
        "name": "anna",
        "cards": ["10D", None, "10C", None, "5C", "8D", "2C"],
        "order": 0,
        "yielded": False,
    }


def test_card_count_and_had_cards_in_round(player):
    kwargs = {"name": "anna", "order": 0}

    player = Player(cards=["10D"], **kwargs)
    assert player.card_count() == 1
    assert player.had_cards_in_round()

    player = Player(cards=[None], **kwargs)
    assert player.card_count() == 0
    assert player.had_cards_in_round()

    player = Player(cards=[], **kwargs)
    assert player.card_count() == 0
    assert not player.had_cards_in_round()


@pytest.fixture
def mocked_draw_cards(get_draw_pile_cards):
    return get_draw_pile_cards(["2S", "5C", "8D", "2C", "AS"])


def test_draw_from_pile(mocked_draw_cards):
    player = Player(name="anna", cards=["10D", None, "10C"], order=0)
    draw_pile = DrawPile(drawn_cards=[], lowest_rank="2", seed=0.4)
    player.draw(draw_pile=draw_pile)
    assert player.serialize() == {
        "name": "anna",
        "cards": ["10D", "10C", "2S", "5C", "8D", "2C"],
        "order": 0,
        "yielded": False,
    }
    assert draw_pile.serialize() == {
        "cards_left": 1,
        "drawn_cards": set(["2S", "5C", "8D", "2C"]),
        "lowest_rank": "2",
        "seed": 0.4,
    }
