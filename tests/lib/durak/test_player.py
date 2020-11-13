import pytest

from lib.durak.draw_pile import DrawPile
from lib.durak.player import Player


@pytest.fixture
def player():
    return Player(
        id="anna",
        hand=["10D", "10C", "2S", "5C", "8D", "2C"],
        order=0,
    )


def test_serialize(player):
    assert player.serialize() == {
        "id": "anna",
        "hand": ["10D", "10C", "2S", "5C", "8D", "2C"],
        "order": 0,
        "state": set(),
    }


def test_card_count(player):
    assert player.card_count() == 6


def test_take_cards(player):
    player.take_cards(cards=["3S", "4D"])
    assert player.serialize() == {
        "id": "anna",
        "hand": ["10D", "10C", "2S", "5C", "8D", "2C", "3S", "4D"],
        "order": 0,
        "state": set(),
    }


def test_remove_card(player):
    player.remove_card(card="2S")
    assert player.serialize() == {
        "id": "anna",
        "hand": ["10D", "10C", "5C", "8D", "2C"],
        "order": 0,
        "state": set(),
    }


def test_card_count_and_had_cards_in_round(player):
    kwargs = {"id": "anna", "order": 0}

    player = Player(hand=["10D"], **kwargs)
    assert player.card_count() == 1
    assert player.had_cards_in_round()

    player = Player(hand=[None], **kwargs)
    assert player.card_count() == 0
    assert player.had_cards_in_round()

    player = Player(hand=[], **kwargs)
    assert player.card_count() == 0
    assert not player.had_cards_in_round()


@pytest.fixture
def mocked_draw_cards(get_draw_pile_cards):
    return get_draw_pile_cards(["2S", "5C", "8D", "2C", "AS"])


def test_draw_from_pile(mocked_draw_cards):
    player = Player(id="anna", hand=["10D", "10C"], order=0)
    draw_pile = DrawPile(drawn_cards=[], lowest_rank="2", seed=0.4)
    player.draw(draw_pile=draw_pile)
    assert player.serialize() == {
        "id": "anna",
        "hand": ["10D", "10C", "2S", "5C", "8D", "2C"],
        "order": 0,
        "state": set(),
    }
    assert draw_pile.serialize() == {
        "cards_left": 1,
        "drawn_cards": set(["2S", "5C", "8D", "2C"]),
        "last_card": "AS",
        "lowest_rank": "2",
        "seed": 0.4,
        "trump_suit": "spades",
    }
