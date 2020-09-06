import pytest

from lib.durak.game import Game


@pytest.fixture
def static_parameters():
    return {
        "lowest_rank": "6",
        "attack_limit": 6,
        "with_passing": True,
    }


@pytest.fixture
def game(static_parameters):
    return Game.deserialize(
        {
            "draw_pile": ["JC", "3S", "6C"],
            "hands": {"anna": ["10D", None, "10C", "2S", "5C", "8D", "2C"]},
            "pass_count": 0,
            "players": ["anna"],
            "table": [],
            "trump_suit": "diamonds",
            "yielded": [],
            **static_parameters,
        }
    )


def test_serialize(game, static_parameters):
    assert game.serialize() == {
        "attackers": ["anna"],
        "defender": None,
        "draw_pile": ["JC", "3S", "6C"],
        "durak": "anna",
        "hands": {"anna": ["10D", None, "10C", "2S", "5C", "8D", "2C"]},
        "legal_attacks": {"cards": set([]), "limit": 0},
        "legal_defenses": {},
        "legal_passes": {"cards": set([]), "limit": 0},
        "pass_count": 0,
        "players": ["anna"],
        "table": [],
        "trump_suit": "diamonds",
        "winners": set(),
        "yielded": [],
        **static_parameters,
    }


def test_attack(game, static_parameters):
    game.attack(player="anna", cards=["10D"])
    assert game.serialize() == {
        "attackers": ["anna"],
        "defender": None,
        "draw_pile": ["JC", "3S", "6C"],
        "durak": "anna",
        "hands": {"anna": [None, None, "10C", "2S", "5C", "8D", "2C"]},
        "legal_attacks": {"cards": set([]), "limit": 0},
        "legal_defenses": {},
        "legal_passes": {"cards": set([]), "limit": 0},
        "pass_count": 0,
        "players": ["anna"],
        "table": [["10D"]],
        "trump_suit": "diamonds",
        "winners": set(),
        "yielded": [],
        **static_parameters,
    }


def test_defend(game, static_parameters):
    game._table.add_card(card="9D")
    game.defend(
        base_card="9D", player="anna", card="10D",
    )
    assert game.serialize() == {
        "attackers": ["anna"],
        "defender": None,
        "draw_pile": ["JC", "3S", "6C"],
        "durak": "anna",
        "hands": {"anna": [None, None, "10C", "2S", "5C", "8D", "2C"]},
        "legal_attacks": {"cards": set([]), "limit": 0},
        "legal_defenses": {},
        "legal_passes": {"cards": set([]), "limit": 0},
        "pass_count": 0,
        "players": ["anna"],
        "table": [["9D", "10D"]],
        "trump_suit": "diamonds",
        "winners": set(),
        "yielded": [],
        **static_parameters,
    }


def test_durak(game, static_parameters):
    game._draw_pile.draw(3)
    assert game.serialize() == {
        "attackers": ["anna"],
        "defender": None,
        "draw_pile": [],
        "durak": "anna",
        "hands": {"anna": ["10D", None, "10C", "2S", "5C", "8D", "2C"]},
        "legal_attacks": {"cards": set([]), "limit": 0},
        "legal_defenses": {},
        "legal_passes": {"cards": set([]), "limit": 0},
        "pass_count": 0,
        "players": ["anna"],
        "table": [],
        "trump_suit": "diamonds",
        "winners": set(),
        "yielded": [],
        **static_parameters,
    }


@pytest.fixture
def game_3p(static_parameters):
    return Game.deserialize(
        {
            "draw_pile": ["7D", "9C", "9D", "10C", "8D"],
            "hands": {
                "anna": ["9H", "3S", "KH", "4C", "4H", None],
                "vasyl": ["7C", "6D", "JS", "7H", None, None],
                "igor": ["8H", "JD", "KS", "5H", "JC", None],
            },
            "pass_count": 0,
            "players": ["anna", "vasyl", "igor"],
            "table": [],
            "trump_suit": "diamonds",
            "yielded": [],
            **static_parameters,
        }
    )


def test_draw(game_3p, static_parameters):
    game_3p.draw()
    assert game_3p.serialize() == {
        "attackers": ["anna"],
        "defender": "vasyl",
        "draw_pile": ["8D"],
        "durak": None,
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
        "legal_passes": {"cards": set([]), "limit": 6},
        "pass_count": 0,
        "players": ["anna", "vasyl", "igor"],
        "table": [],
        "trump_suit": "diamonds",
        "winners": set(),
        "yielded": [],
        **static_parameters,
    }


def test_draw_with_pass_count(game_3p, static_parameters):
    game_3p._pass_count = 2
    game_3p.draw()
    assert game_3p.serialize() == {
        "attackers": ["anna"],
        "defender": "vasyl",
        "draw_pile": ["8D"],
        "durak": None,
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
        "legal_passes": {"cards": set([]), "limit": 6},
        "pass_count": 0,
        "players": ["anna", "vasyl", "igor"],
        "table": [],
        "trump_suit": "diamonds",
        "winners": set(),
        "yielded": [],
        **static_parameters,
    }


def test_legal_defenses(game_3p, static_parameters):
    game_3p._table.add_card(card="10S")
    assert game_3p.serialize() == {
        "attackers": ["anna", "igor"],
        "defender": "vasyl",
        "draw_pile": ["7D", "9C", "9D", "10C", "8D"],
        "durak": None,
        "hands": {
            "anna": ["9H", "3S", "KH", "4C", "4H", None],
            "vasyl": ["7C", "6D", "JS", "7H", None, None],
            "igor": ["8H", "JD", "KS", "5H", "JC", None],
        },
        "pass_count": 0,
        "legal_attacks": {"cards": set([]), "limit": 3},
        "legal_defenses": {"10S": set(["JS", "6D"])},
        "legal_passes": {"cards": set([]), "limit": 4},
        "players": ["anna", "vasyl", "igor"],
        "table": [["10S"]],
        "trump_suit": "diamonds",
        "winners": set(),
        "yielded": [],
        **static_parameters,
    }


def test_legal_attacks(game_3p, static_parameters):
    game_3p._table.add_card(card="4S")
    assert game_3p.serialize() == {
        "attackers": ["anna", "igor"],
        "defender": "vasyl",
        "draw_pile": ["7D", "9C", "9D", "10C", "8D"],
        "durak": None,
        "hands": {
            "anna": ["9H", "3S", "KH", "4C", "4H", None],
            "vasyl": ["7C", "6D", "JS", "7H", None, None],
            "igor": ["8H", "JD", "KS", "5H", "JC", None],
        },
        "pass_count": 0,
        "legal_attacks": {"cards": set(["4C", "4H"]), "limit": 3},
        "legal_defenses": {"4S": set(["JS", "6D"])},
        "legal_passes": {"cards": set([]), "limit": 4},
        "players": ["anna", "vasyl", "igor"],
        "table": [["4S"]],
        "trump_suit": "diamonds",
        "winners": set(),
        "yielded": [],
        **static_parameters,
    }


def test_legal_passes(game_3p, static_parameters):
    game_3p._table.add_card(card="7S")
    assert game_3p.serialize() == {
        "attackers": ["anna", "igor"],
        "defender": "vasyl",
        "draw_pile": ["7D", "9C", "9D", "10C", "8D"],
        "durak": None,
        "hands": {
            "anna": ["9H", "3S", "KH", "4C", "4H", None],
            "vasyl": ["7C", "6D", "JS", "7H", None, None],
            "igor": ["8H", "JD", "KS", "5H", "JC", None],
        },
        "pass_count": 0,
        "legal_attacks": {"cards": set([]), "limit": 3},
        "legal_defenses": {"7S": set(["JS", "6D"])},
        "legal_passes": {"cards": set(["7C", "7H"]), "limit": 4},
        "players": ["anna", "vasyl", "igor"],
        "table": [["7S"]],
        "trump_suit": "diamonds",
        "winners": set(),
        "yielded": [],
        **static_parameters,
    }


def test_legal_passes_when_on_deck_defender_has_no_cards(game_3p, static_parameters):
    game_3p._table.add_card(card="7S")

    for card in ["8H", "JD", "KS", "5H", "JC"]:
        game_3p._player("igor").remove_card(card=card)

    assert game_3p.serialize() == {
        "attackers": ["anna"],
        "defender": "vasyl",
        "draw_pile": ["7D", "9C", "9D", "10C", "8D"],
        "durak": None,
        "hands": {
            "anna": ["9H", "3S", "KH", "4C", "4H", None],
            "vasyl": ["7C", "6D", "JS", "7H", None, None],
            "igor": [None, None, None, None, None, None],
        },
        "pass_count": 0,
        "legal_attacks": {"cards": set([]), "limit": 3},
        "legal_defenses": {"7S": set(["JS", "6D"])},
        "legal_passes": {"cards": set(["7C", "7H"]), "limit": 4},
        "players": ["anna", "vasyl", "igor"],
        "table": [["7S"]],
        "trump_suit": "diamonds",
        "winners": set(),
        "yielded": [],
        **static_parameters,
    }
