import json

import pytest

from lib.durak import attack_with_many, pass_with_many, yield_attack
from lib.durak.game import Game
from main import handle_durak_message


@pytest.fixture
def assert_message(mocker):
    mocked_persist = mocker.patch("main.persist")

    async def wrapped(from_state, to_state):
        result = await handle_durak_message(from_state)
        assert json.loads(result) == json.loads(to_state)
        mocked_persist.assert_called_once()

    return wrapped


@pytest.mark.asyncio
async def test_start_game(assert_message):
    await assert_message(
        json.dumps(
            {
                "type": "started_game",
                "from_state": {
                    "draw_pile": [
                        "10C",
                        "QC",
                        "JS",
                        "6S",
                        "9D",
                        "7S",
                        "QD",
                        "AS",
                        "10D",
                        "7H",
                        "10S",
                        "9C",
                        "KC",
                        "9H",
                        "QH",
                        "JC",
                        "8H",
                        "10H",
                        "QS",
                        "KH",
                        "AD",
                        "KD",
                        "JH",
                        "8S",
                        "AH",
                        "6C",
                        "7C",
                        "7D",
                        "6D",
                        "6H",
                        "AC",
                        "8D",
                        "9S",
                        "KS",
                        "8C",
                        "JD",
                    ],
                    "hands": {"anna": [], "vasyl": [], "igor": [], "grusha": []},
                    "players": ["anna", "vasyl", "igor", "grusha"],
                    "pass_count": 0,
                    "table": [],
                    "trump_suit": "diamonds",
                    "yielded": [],
                    "lowest_rank": "6",
                    "attack_limit": 100,
                    "with_passing": True,
                    "durak": None,
                    "collector": None,
                },
                "user": "anna",
                "payload": {},
            }
        ),
        json.dumps(
            {
                "type": "started_game",
                "to_state": {
                    "durak": None,
                    "hands": {
                        "anna": ["10C", "QC", "JS", "6S", "9D", "7S"],
                        "igor": ["KC", "9H", "QH", "JC", "8H", "10H"],
                        "vasyl": ["QD", "AS", "10D", "7H", "10S", "9C"],
                        "grusha": ["QS", "KH", "AD", "KD", "JH", "8S"],
                    },
                    "table": [],
                    "players": ["anna", "vasyl", "igor", "grusha"],
                    "winners": [],
                    "yielded": [],
                    "defender": "vasyl",
                    "attackers": ["anna"],
                    "draw_pile": [
                        "AH",
                        "6C",
                        "7C",
                        "7D",
                        "6D",
                        "6H",
                        "AC",
                        "8D",
                        "9S",
                        "KS",
                        "8C",
                        "JD",
                    ],
                    "pass_count": 0,
                    "trump_suit": "diamonds",
                    "lowest_rank": "6",
                    "attack_limit": 100,
                    "legal_passes": {"cards": [], "limit": 6},
                    "with_passing": True,
                    "legal_attacks": {
                        "cards": sorted(["QC", "10C", "JS", "6S", "7S", "9D"]),
                        "limit": 6,
                    },
                    "legal_defenses": {},
                    "collector": None,
                },
                "user": "anna",
                "payload": {},
            }
        ),
    )


def test_pass_with_last_card():
    assert pass_with_many(
        from_state={
            "hands": {
                "anna": ["10H"],
                "igor": ["9S", "QC"],
                "vasyl": ["AH", "10C"],
                "grusha": ["QS", None, "KH"],
            },
            "table": [["10D"]],
            "players": ["grusha", "anna", "vasyl", "igor"],
            "yielded": [],
            "draw_pile": [],
            "pass_count": 0,
            "trump_suit": "hearts",
            "lowest_rank": "6",
            "attack_limit": 100,
            "with_passing": True,
            "durak": None,
            "collector": None,
        },
        user="anna",
        payload={"cards": ["10H"]},
    ) == {
        "durak": None,
        "hands": {
            "anna": [None],
            "igor": ["9S", "QC"],
            "vasyl": ["AH", "10C"],
            "grusha": ["QS", None, "KH"],
        },
        "table": [["10D"], ["10H"]],
        "players": ["anna", "vasyl", "igor", "grusha"],
        "winners": set(["anna"]),
        "yielded": [],
        "defender": "vasyl",
        "attackers": ["igor", "grusha"],
        "draw_pile": [],
        "pass_count": 1,
        "trump_suit": "hearts",
        "lowest_rank": "6",
        "attack_limit": 100,
        "legal_passes": {"cards": set(["10C"]), "limit": 0},
        "with_passing": True,
        "legal_attacks": {"cards": set(), "limit": 0},
        "legal_defenses": {"10D": set(["AH"]), "10H": set(["AH"])},
        "collector": None,
    }


def test_defend_successfully_after_attack_plays_last_card():
    assert yield_attack(
        from_state={
            "hands": {
                "anna": ["KS", None, None, None, "JD", None],
                "igor": ["9S", "QD", None, "6S", "6D", "JS"],
                "vasyl": ["JC", "QS", "8C", "QH", None, "6H"],
                "grusha": [None, None],
            },
            "table": [["8H", "AH"], ["8D", "AD"], ["AC", "7S"], ["8S", "AS"]],
            "players": ["grusha", "anna", "vasyl", "igor"],
            "yielded": ["vasyl"],
            "draw_pile": [],
            "pass_count": 0,
            "trump_suit": "spades",
            "lowest_rank": "6",
            "attack_limit": 100,
            "with_passing": True,
            "durak": None,
            "collector": None,
        },
        user="igor",
        payload={},
    ) == {
        "durak": None,
        "hands": {
            "anna": ["KS", "JD"],
            "igor": ["9S", "QD", "6S", "6D", "JS"],
            "vasyl": ["JC", "QS", "8C", "QH", "6H"],
            "grusha": [],
        },
        "table": [],
        "players": ["anna", "vasyl", "igor", "grusha"],
        "winners": set(["grusha"]),
        "yielded": [],
        "defender": "vasyl",
        "attackers": ["anna"],
        "draw_pile": [],
        "pass_count": 0,
        "trump_suit": "spades",
        "lowest_rank": "6",
        "attack_limit": 100,
        "legal_passes": {"cards": set([]), "limit": 5},
        "with_passing": True,
        "legal_attacks": {"cards": set(["KS", "JD"]), "limit": 5},
        "legal_defenses": {},
        "collector": None,
    }


def test_collect_rotates_properly():
    assert yield_attack(
        from_state={
            "hands": {
                "anna": [None],
                "igor": ["9S", "6S", "6D", "JD", "QD", "JC", "JS", "QH", "QS"],
                "vasyl": ["8C", "6H"],
                "grusha": [],
            },
            "table": [["KS"]],
            "players": ["anna", "vasyl", "igor", "grusha"],
            "yielded": ["igor", "grusha"],
            "draw_pile": [],
            "pass_count": 0,
            "trump_suit": "spades",
            "lowest_rank": "6",
            "attack_limit": 100,
            "with_passing": True,
            "durak": None,
            "collector": "vasyl",
        },
        user="anna",
        payload={},
    ) == {
        "durak": None,
        "hands": {
            "anna": [],
            "igor": ["9S", "6S", "6D", "JD", "QD", "JC", "JS", "QH", "QS"],
            "vasyl": ["8C", "6H", "KS"],
            "grusha": [],
        },
        "table": [],
        "players": ["igor", "anna", "vasyl", "grusha"],
        "winners": set(["anna", "grusha"]),
        "yielded": [],
        "defender": "vasyl",
        "attackers": ["igor"],
        "draw_pile": [],
        "pass_count": 0,
        "trump_suit": "spades",
        "lowest_rank": "6",
        "attack_limit": 100,
        "legal_passes": {"cards": set([]), "limit": 9},
        "with_passing": True,
        "legal_attacks": {
            "cards": set(["QS", "JS", "9S", "JD", "QD", "JC", "6D", "QH", "6S"]),
            "limit": 3,
        },
        "legal_defenses": {},
        "collector": None,
    }


def test_yielding_when_defender_wins():
    assert yield_attack(
        from_state={
            "hands": {
                "anna": [None, None, None, None],
                "igor": ["KC", None, "6D"],
                "vasyl": ["AC", "8H", "10D", None, "AS", None, "9C", "9H", "QD", "9S"],
                "grusha": [None, "KH", "AD", "KD", "JH"],
            },
            "table": [["QH", "8D"], ["QS", "KS"], ["8C", "9D"], ["8S", "JD"]],
            "players": ["grusha", "anna", "vasyl", "igor"],
            "yielded": ["vasyl", "igor"],
            "draw_pile": [],
            "pass_count": 1,
            "trump_suit": "diamonds",
            "lowest_rank": "6",
            "attack_limit": 100,
            "with_passing": True,
            "durak": None,
            "collector": None,
        },
        payload={},
        user="grusha",
    ) == {
        "hands": {
            "anna": [],
            "igor": ["KC", "6D"],
            "vasyl": ["AC", "8H", "10D", "AS", "9C", "9H", "QD", "9S"],
            "grusha": ["KH", "AD", "KD", "JH"],
        },
        "table": [],
        "players": ["anna", "vasyl", "igor", "grusha"],
        "winners": set(["anna"]),
        "yielded": [],
        "defender": "igor",
        "attackers": ["vasyl"],
        "draw_pile": [],
        "pass_count": 0,
        "trump_suit": "diamonds",
        "lowest_rank": "6",
        "attack_limit": 100,
        "legal_passes": {"cards": set(), "limit": 4},
        "with_passing": True,
        "legal_attacks": {
            "cards": set(["9C", "AS", "9H", "9S", "QD", "AC", "8H", "10D"]),
            "limit": 2,
        },
        "legal_defenses": {},
        "durak": None,
        "collector": None,
    }


def test_cannot_attack_with_unmatched_rank():
    with pytest.raises(Game.DifferentRanks):
        attack_with_many(
            from_state={
                "durak": None,
                "hands": {
                    "john": ["KC", "KH", "QC", "JS", "6S", "7C"],
                    "cyril": [
                        "QH",
                        "6C",
                        "JC",
                        "6D",
                        "7D",
                        "7H",
                        "JH",
                        "7S",
                        "AS",
                        "JD",
                        "KD",
                        "AH",
                    ],
                    "kevin": ["AC", "AD", "KS", "QD", "6H", "QS"],
                    "maxim": [
                        "10H",
                        "8S",
                        "9S",
                        "8C",
                        "9C",
                        "8H",
                        "9H",
                        "8D",
                        "10D",
                        "9D",
                        "10C",
                        "10S",
                    ],
                },
                "table": [],
                "players": ["cyril", "kevin", "john", "maxim"],
                "winners": [],
                "yielded": [],
                "defender": "kevin",
                "attackers": ["cyril"],
                "collector": None,
                "draw_pile": [],
                "pass_count": 0,
                "trump_suit": "clubs",
                "lowest_rank": "6",
                "attack_limit": 6,
                "legal_passes": {"cards": [], "limit": 6},
                "with_passing": True,
                "legal_attacks": {
                    "cards": [
                        "QH",
                        "7D",
                        "JH",
                        "6D",
                        "JC",
                        "AS",
                        "JD",
                        "7H",
                        "7S",
                        "AH",
                        "6C",
                        "KD",
                    ],
                    "limit": 6,
                },
                "legal_defenses": {},
            },
            payload={"cards": ["KD", "6D"]},
            user="cyril",
        )
