import pytest

from lib.durak.game import Game


@pytest.fixture
def game():
    return Game.deserialize(
        draw_pile=["JC", "3S", "6C"],
        hands={"anna": ["10D", None, "10C", "2S", "5C", "8D", "2C"]},
        pass_count=0,
        players=["anna"],
        table=[],
        yielded=[],
    )


def test_serialize(game):
    assert game.serialize() == {
        "draw_pile": ["JC", "3S", "6C"],
        "hands": {"anna": ["10D", None, "10C", "2S", "5C", "8D", "2C"]},
        "legal_defenses": {},
        "pass_count": 0,
        "players": ["anna"],
        "table": [],
        "yielded": [],
    }


def test_attack(game):
    game.attack(player="anna", card="10D")
    assert game.serialize() == {
        "draw_pile": ["JC", "3S", "6C"],
        "hands": {"anna": [None, None, "10C", "2S", "5C", "8D", "2C"]},
        "legal_defenses": {},
        "pass_count": 0,
        "players": ["anna"],
        "table": [["10D"]],
        "yielded": [],
    }


def test_defend(game):
    nine_of_D = "9D"
    game._table.add_card(card=nine_of_D)
    game.defend(
        base_card=nine_of_D, player="anna", card="10D",
    )
    assert game.serialize() == {
        "draw_pile": ["JC", "3S", "6C"],
        "hands": {"anna": [None, None, "10C", "2S", "5C", "8D", "2C"]},
        "legal_defenses": {},
        "pass_count": 0,
        "players": ["anna"],
        "table": [[nine_of_D, "10D"]],
        "yielded": [],
    }


@pytest.fixture
def game_3p():
    return Game.deserialize(
        draw_pile=["7D", "9C", "9D", "10C", "8D"],
        hands={
            "anna": ["9H", "3S", "KH", "4C", "4H", None],
            "vasyl": ["7C", "6D", "JS", "7H", None, None],
            "igor": ["8H", "JD", "KS", "5H", "JC", None],
        },
        pass_count=0,
        players=["anna", "vasyl", "igor"],
        table=[],
        yielded=[],
    )


def test_draw(game_3p):
    game_3p.draw()
    assert game_3p.serialize() == {
        "draw_pile": ["8D"],
        "hands": {
            "anna": ["9H", "3S", "KH", "4C", "4H", "7D"],
            "vasyl": ["7C", "6D", "JS", "7H", "9C", "9D"],
            "igor": ["8H", "JD", "KS", "5H", "JC", "10C"],
        },
        "legal_defenses": {},
        "pass_count": 0,
        "players": ["anna", "vasyl", "igor"],
        "table": [],
        "yielded": [],
    }


def test_draw_with_pass_count(game_3p):
    game_3p._pass_count = 2
    game_3p.draw()
    assert game_3p.serialize() == {
        "draw_pile": ["8D"],
        "hands": {
            "anna": ["9H", "3S", "KH", "4C", "4H", "10C"],
            "vasyl": ["7C", "6D", "JS", "7H", "7D", "9C"],
            "igor": ["8H", "JD", "KS", "5H", "JC", "9D"],
        },
        "legal_defenses": {},
        "pass_count": 0,
        "players": ["anna", "vasyl", "igor"],
        "table": [],
        "yielded": [],
    }


def test_legal_defenses(game_3p):
    game_3p._table.add_card(card="10S")
    assert game_3p.serialize() == {
        "draw_pile": ["7D", "9C", "9D", "10C", "8D"],
        "hands": {
            "anna": ["9H", "3S", "KH", "4C", "4H", None],
            "vasyl": ["7C", "6D", "JS", "7H", None, None],
            "igor": ["8H", "JD", "KS", "5H", "JC", None],
        },
        "pass_count": 0,
        "legal_defenses": {"10S": set(["JS", "6D"])},
        "players": ["anna", "vasyl", "igor"],
        "table": [["10S"]],
        "yielded": [],
    }
