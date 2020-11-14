from datetime import datetime

import pytest
from freezegun import freeze_time

from lib.durak.game import Game, Status


@pytest.fixture
def from_epoch():
    with freeze_time(datetime.utcfromtimestamp(0)):
        yield


@pytest.fixture
def static_parameters():
    return {
        "attack_limit": "hand",
        "lowest_rank": "2",
        "seed": 0.4,
        "with_passing": True,
    }


@pytest.fixture
def mocked_draw_cards(get_draw_pile_cards):
    return get_draw_pile_cards(["JC", "3S", "6C"])


@pytest.fixture
def game(mocked_draw_cards, static_parameters):
    return Game.deserialize(
        {
            "drawn_cards": [],
            "pass_count": 0,
            "players": [
                {
                    "id": "anna",
                    "hand": ["10D", "10C", "2S", "5C", "8D", "2C"],
                    "order": 0,
                    "state": [],
                    "organize_strategy": "no_sort",
                    "attacks": [],
                }
            ],
            "table": [],
            "trump_suit": "clubs",
            **static_parameters,
        }
    )


def test_serialize(game, static_parameters):
    assert game.serialize() == {
        "attackers": ["anna"],
        "cards_left": 3,
        "drawn_cards": set(),
        "defender": None,
        "last_card": "6C",
        "legal_attacks": {"cards": set([]), "limit": 0},
        "legal_defenses": {},
        "legal_passes": {"cards": set([]), "limit": 0},
        "pass_count": 0,
        "players": [
            {
                "order": 0,
                "id": "anna",
                "hand": ["10D", "10C", "2S", "5C", "8D", "2C"],
                "state": set([Status.DURAK]),
                "organize_strategy": "no_sort",
                "attacks": [],
            }
        ],
        "table": [],
        "trump_suit": "clubs",
        "winners": set(),
        **static_parameters,
    }


def test_attack(from_epoch, game, static_parameters):
    game.attack(player="anna", cards=["10D"])
    assert game.serialize() == {
        "attackers": ["anna"],
        "cards_left": 3,
        "defender": None,
        "drawn_cards": set(),
        "last_card": "6C",
        "legal_attacks": {"cards": set([]), "limit": 0},
        "legal_defenses": {},
        "legal_passes": {"cards": set([]), "limit": 0},
        "pass_count": 0,
        "players": [
            {
                "order": 0,
                "id": "anna",
                "hand": ["10C", "2S", "5C", "8D", "2C"],
                "state": set([Status.DURAK]),
                "organize_strategy": "no_sort",
                "attacks": [{"attack": "10D", "defense": None, "timestamp": 0}],
            }
        ],
        "table": [["10D"]],
        "trump_suit": "clubs",
        "winners": set(),
        **static_parameters,
    }


def test_defend(from_epoch, game, static_parameters):
    game.attack(player=game.player("anna"), cards=["8D"])
    game.defend(
        base_card="8D",
        player="anna",
        card="10D",
    )
    assert game.serialize() == {
        "attackers": ["anna"],
        "cards_left": 3,
        "defender": None,
        "drawn_cards": set(),
        "last_card": "6C",
        "legal_attacks": {"cards": set([]), "limit": 0},
        "legal_defenses": {},
        "legal_passes": {"cards": set([]), "limit": 0},
        "pass_count": 0,
        "players": [
            {
                "order": 0,
                "id": "anna",
                "hand": ["10C", "2S", "5C", "2C"],
                "state": set([Status.DURAK]),
                "organize_strategy": "no_sort",
                "attacks": [{"attack": "8D", "defense": "10D", "timestamp": 0}],
            }
        ],
        "table": [["8D", "10D"]],
        "trump_suit": "clubs",
        "winners": set(),
        **static_parameters,
    }


def test_durak(game, static_parameters):
    game._draw_pile.draw(3)
    assert game.serialize() == {
        "attackers": ["anna"],
        "cards_left": 0,
        "defender": None,
        "drawn_cards": set(["JC", "3S", "6C"]),
        "last_card": "6C",
        "legal_attacks": {"cards": set([]), "limit": 0},
        "legal_defenses": {},
        "legal_passes": {"cards": set([]), "limit": 0},
        "pass_count": 0,
        "players": [
            {
                "order": 0,
                "id": "anna",
                "hand": ["10D", "10C", "2S", "5C", "8D", "2C"],
                "state": set([Status.DURAK]),
                "organize_strategy": "no_sort",
                "attacks": [],
            }
        ],
        "table": [],
        "trump_suit": "clubs",
        "winners": set(),
        **static_parameters,
    }


@pytest.fixture
def mocked_draw_cards_3p(get_draw_pile_cards):
    return get_draw_pile_cards(["7D", "9C", "9D", "10C", "8D"])


@pytest.fixture
def game_3p(mocked_draw_cards_3p, static_parameters):
    return Game.deserialize(
        {
            "drawn_cards": [],
            "pass_count": 0,
            "players": [
                {
                    "order": 0,
                    "id": "anna",
                    "hand": ["9H", "3S", "KH", "4C", "4H"],
                    "state": [],
                    "organize_strategy": "no_sort",
                    "attacks": [],
                },
                {
                    "order": 1,
                    "id": "vasyl",
                    "hand": ["7C", "6D", "JS", "7H"],
                    "state": [],
                    "organize_strategy": "no_sort",
                    "attacks": [],
                },
                {
                    "order": 2,
                    "id": "igor",
                    "hand": ["8H", "JD", "KS", "5H", "JC"],
                    "state": [],
                    "organize_strategy": "no_sort",
                    "attacks": [],
                },
            ],
            "table": [],
            "trump_suit": "diamonds",
            **static_parameters,
        }
    )


def test_draw(game_3p, static_parameters):
    game_3p.draw()
    assert game_3p.serialize() == {
        "attackers": ["anna"],
        "cards_left": 1,
        "drawn_cards": set(["7D", "9C", "9D", "10C"]),
        "defender": "vasyl",
        "last_card": "8D",
        "legal_attacks": {
            "cards": set(["9H", "3S", "KH", "4C", "4H", "7D"]),
            "limit": 6,
        },
        "legal_defenses": {},
        "legal_passes": {"cards": set([]), "limit": 6},
        "pass_count": 0,
        "players": [
            {
                "order": 0,
                "id": "anna",
                "hand": ["9H", "3S", "KH", "4C", "4H", "7D"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
            {
                "order": 1,
                "id": "vasyl",
                "hand": ["7C", "6D", "JS", "7H", "9C", "9D"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
            {
                "order": 2,
                "id": "igor",
                "hand": ["8H", "JD", "KS", "5H", "JC", "10C"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
        ],
        "table": [],
        "trump_suit": "diamonds",
        "winners": set(),
        **static_parameters,
    }


def test_draw_with_pass_count(game_3p, static_parameters):
    game_3p._pass_count = 2
    game_3p.draw()
    assert game_3p.serialize() == {
        "attackers": ["anna"],
        "cards_left": 1,
        "defender": "vasyl",
        "drawn_cards": set(["7D", "9C", "9D", "10C"]),
        "last_card": "8D",
        "legal_attacks": {
            "cards": set(["9H", "3S", "KH", "4C", "4H", "10C"]),
            "limit": 6,
        },
        "legal_defenses": {},
        "legal_passes": {"cards": set([]), "limit": 6},
        "pass_count": 0,
        "players": [
            {
                "order": 0,
                "id": "anna",
                "hand": ["9H", "3S", "KH", "4C", "4H", "10C"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
            {
                "order": 1,
                "id": "vasyl",
                "hand": ["7C", "6D", "JS", "7H", "7D", "9C"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
            {
                "order": 2,
                "id": "igor",
                "hand": ["8H", "JD", "KS", "5H", "JC", "9D"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
        ],
        "table": [],
        "trump_suit": "diamonds",
        "winners": set(),
        **static_parameters,
    }


def test_legal_defenses(from_epoch, game_3p, static_parameters):
    anna = game_3p.player("anna")
    anna.take_cards(cards=["10S"])
    game_3p.attack(player=anna, cards=["10S"])
    assert game_3p.serialize() == {
        "attackers": ["anna", "igor"],
        "cards_left": 5,
        "defender": "vasyl",
        "drawn_cards": set(),
        "pass_count": 0,
        "last_card": "8D",
        "legal_attacks": {"cards": set([]), "limit": 3},
        "legal_defenses": {"10S": set(["JS", "6D"])},
        "legal_passes": {"cards": set([]), "limit": 4},
        "players": [
            {
                "order": 0,
                "id": "anna",
                "hand": ["9H", "3S", "KH", "4C", "4H"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [{"attack": "10S", "defense": None, "timestamp": 0}],
            },
            {
                "order": 1,
                "id": "vasyl",
                "hand": ["7C", "6D", "JS", "7H"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
            {
                "order": 2,
                "id": "igor",
                "hand": ["8H", "JD", "KS", "5H", "JC"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
        ],
        "table": [["10S"]],
        "trump_suit": "diamonds",
        "winners": set(),
        **static_parameters,
    }


def test_legal_attacks(from_epoch, game_3p, static_parameters):
    anna = game_3p.player("anna")
    anna.take_cards(cards=["4S"])
    game_3p.attack(player=anna, cards=["4S"])
    assert game_3p.serialize() == {
        "attackers": ["anna", "igor"],
        "cards_left": 5,
        "defender": "vasyl",
        "drawn_cards": set(),
        "pass_count": 0,
        "last_card": "8D",
        "legal_attacks": {"cards": set(["4C", "4H"]), "limit": 3},
        "legal_defenses": {"4S": set(["JS", "6D"])},
        "legal_passes": {"cards": set([]), "limit": 4},
        "players": [
            {
                "order": 0,
                "id": "anna",
                "hand": ["9H", "3S", "KH", "4C", "4H"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [{"attack": "4S", "defense": None, "timestamp": 0}],
            },
            {
                "order": 1,
                "id": "vasyl",
                "hand": ["7C", "6D", "JS", "7H"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
            {
                "order": 2,
                "id": "igor",
                "hand": ["8H", "JD", "KS", "5H", "JC"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
        ],
        "table": [["4S"]],
        "trump_suit": "diamonds",
        "winners": set(),
        **static_parameters,
    }


def test_legal_passes(from_epoch, game_3p, static_parameters):
    anna = game_3p.player("anna")
    anna.take_cards(cards=["7S"])
    game_3p.attack(player=anna, cards=["7S"])
    assert game_3p.serialize() == {
        "attackers": ["anna", "igor"],
        "cards_left": 5,
        "defender": "vasyl",
        "drawn_cards": set(),
        "pass_count": 0,
        "last_card": "8D",
        "legal_attacks": {"cards": set([]), "limit": 3},
        "legal_defenses": {"7S": set(["JS", "6D"])},
        "legal_passes": {"cards": set(["7C", "7H"]), "limit": 4},
        "players": [
            {
                "order": 0,
                "id": "anna",
                "hand": ["9H", "3S", "KH", "4C", "4H"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [{"attack": "7S", "defense": None, "timestamp": 0}],
            },
            {
                "order": 1,
                "id": "vasyl",
                "hand": ["7C", "6D", "JS", "7H"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
            {
                "order": 2,
                "id": "igor",
                "hand": ["8H", "JD", "KS", "5H", "JC"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
        ],
        "table": [["7S"]],
        "trump_suit": "diamonds",
        "winners": set(),
        **static_parameters,
    }


@pytest.mark.xfail(reason="Attack limit does not exist")
def test_legal_attacks_and_passes_with_limits(game_3p, static_parameters):
    game_3p._table.add_card(card="7S")
    game_3p._attack_limit = 3
    assert game_3p.serialize() == {
        **static_parameters,
        "attackers": ["anna", "igor"],
        "cards_left": 5,
        "attack_limit": 3,
        "defender": "vasyl",
        "drawn_cards": set(),
        "pass_count": 0,
        "last_card": "8D",
        "legal_attacks": {"cards": set([]), "limit": 2},
        "legal_defenses": {"7S": set(["JS", "6D"])},
        "legal_passes": {"cards": set(["7C", "7H"]), "limit": 2},
        "players": [
            {
                "order": 0,
                "id": "anna",
                "hand": ["9H", "3S", "KH", "4C", "4H"],
                "state": set(),
                "organize_strategy": "no_sort",
            },
            {
                "order": 1,
                "id": "vasyl",
                "hand": ["7C", "6D", "JS", "7H"],
                "state": set(),
                "organize_strategy": "no_sort",
            },
            {
                "order": 2,
                "id": "igor",
                "hand": ["8H", "JD", "KS", "5H", "JC"],
                "state": set(),
                "organize_strategy": "no_sort",
            },
        ],
        "seed": 0.4,
        "table": [["7S"]],
        "trump_suit": "diamonds",
        "winners": set(),
    }


def test_legal_passes_when_on_deck_defender_has_no_cards(
    from_epoch, game_3p, static_parameters
):
    anna = game_3p.player("anna")
    anna.take_cards(cards=["7S"])
    game_3p.attack(player=anna, cards=["7S"])

    for card in ["8H", "JD", "KS", "5H", "JC"]:
        game_3p.player("igor").remove_card(card=card)

    assert game_3p.serialize() == {
        "attackers": ["anna"],
        "cards_left": 5,
        "defender": "vasyl",
        "drawn_cards": set(),
        "pass_count": 0,
        "last_card": "8D",
        "legal_attacks": {"cards": set([]), "limit": 3},
        "legal_defenses": {"7S": set(["JS", "6D"])},
        "legal_passes": {"cards": set(["7C", "7H"]), "limit": 4},
        "players": [
            {
                "order": 0,
                "id": "anna",
                "hand": ["9H", "3S", "KH", "4C", "4H"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [{"attack": "7S", "defense": None, "timestamp": 0}],
            },
            {
                "order": 1,
                "id": "vasyl",
                "hand": ["7C", "6D", "JS", "7H"],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
            {
                "order": 2,
                "id": "igor",
                "hand": [],
                "state": set(),
                "organize_strategy": "no_sort",
                "attacks": [],
            },
        ],
        "table": [["7S"]],
        "trump_suit": "diamonds",
        "winners": set(),
        **static_parameters,
    }


def test_durak_persists(game_3p, static_parameters):
    game_3p.player("anna").add_status(Status.DURAK)
    serialized = game_3p.serialize()
    assert Status.DURAK in next(
        player["state"] for player in serialized["players"] if player["id"] == "anna"
    )
