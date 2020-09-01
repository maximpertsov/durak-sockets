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
        trump_suit="diamonds",
        yielded=[],
    )


def test_serialize(game):
    assert game.serialize() == {
        "draw_pile": ["JC", "3S", "6C"],
        "hands": {"anna": ["10D", None, "10C", "2S", "5C", "8D", "2C"]},
        "legal_attacks": {"cards": set([]), "limit": 0},
        "legal_defenses": {},
        "pass_count": 0,
        "players": ["anna"],
        "table": [],
        "trump_suit": "diamonds",
        "yielded": [],
    }


def test_attack(game):
    game.attack(player="anna", card="10D")
    assert game.serialize() == {
        "draw_pile": ["JC", "3S", "6C"],
        "hands": {"anna": [None, None, "10C", "2S", "5C", "8D", "2C"]},
        "legal_attacks": {"cards": set([]), "limit": 0},
        "legal_defenses": {},
        "pass_count": 0,
        "players": ["anna"],
        "table": [["10D"]],
        "trump_suit": "diamonds",
        "yielded": [],
    }


def test_defend(game):
    game._table.add_card(card="9D")
    game.defend(
        base_card="9D", player="anna", card="10D",
    )
    assert game.serialize() == {
        "draw_pile": ["JC", "3S", "6C"],
        "hands": {"anna": [None, None, "10C", "2S", "5C", "8D", "2C"]},
        "legal_attacks": {"cards": set([]), "limit": 0},
        "legal_defenses": {},
        "pass_count": 0,
        "players": ["anna"],
        "table": [["9D", "10D"]],
        "trump_suit": "diamonds",
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
        trump_suit="diamonds",
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
        "legal_attacks": {
            "cards": set(["9H", "3S", "KH", "4C", "4H", "7D"]),
            "limit": 6,
        },
        "legal_defenses": {},
        "pass_count": 0,
        "players": ["anna", "vasyl", "igor"],
        "table": [],
        "trump_suit": "diamonds",
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
        "legal_attacks": {
            "cards": set(["9H", "3S", "KH", "4C", "4H", "10C"]),
            "limit": 6,
        },
        "legal_defenses": {},
        "pass_count": 0,
        "players": ["anna", "vasyl", "igor"],
        "table": [],
        "trump_suit": "diamonds",
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
        "legal_attacks": {"cards": set([]), "limit": 3},
        "legal_defenses": {"10S": set(["JS", "6D"])},
        "players": ["anna", "vasyl", "igor"],
        "table": [["10S"]],
        "trump_suit": "diamonds",
        "yielded": [],
    }


def test_legal_attacks(game_3p):
    game_3p._table.add_card(card="4S")
    assert game_3p.serialize() == {
        "draw_pile": ["7D", "9C", "9D", "10C", "8D"],
        "hands": {
            "anna": ["9H", "3S", "KH", "4C", "4H", None],
            "vasyl": ["7C", "6D", "JS", "7H", None, None],
            "igor": ["8H", "JD", "KS", "5H", "JC", None],
        },
        "pass_count": 0,
        "legal_attacks": {"cards": set(["4C", "4H"]), "limit": 3},
        "legal_defenses": {"4S": set(["JS", "6D"])},
        "players": ["anna", "vasyl", "igor"],
        "table": [["4S"]],
        "trump_suit": "diamonds",
        "yielded": [],
    }


def test_legal_attacks_defender_has_no_cards(game_3p):
    game_3p._table.add_card(card="4S")
    for card in ["7C", "6D", "JS", "7H"]:
        game_3p._player("vasyl").remove_card(card=card)
    assert game_3p.serialize() == {
        "draw_pile": ["7D", "9C", "9D", "10C", "8D"],
        "hands": {
            "anna": ["9H", "3S", "KH", "4C", "4H", None],
            "vasyl": [None, None, None, None, None, None],
            "igor": ["8H", "JD", "KS", "5H", "JC", None],
        },
        "pass_count": 0,
        "legal_attacks": {"cards": set(["4C", "4H"]), "limit": 0},
        "legal_defenses": {"4S": set([])},
        "players": ["anna", "vasyl", "igor"],
        "table": [["4S"]],
        "trump_suit": "diamonds",
        "yielded": [],
    }
