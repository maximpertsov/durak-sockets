import glob
import json
import os

import pytest

from lib.durak import attack_with_many, yield_attack
from lib.durak.game import Game
from main import handle_durak_message

SCENARIO_INPUT_FILES = glob.glob(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "scenario_inputs", "*.json"
    )
)


@pytest.fixture
def assert_handle_message(mocker):
    mocked_persist = mocker.patch("main.persist")

    async def wrapped(from_state, to_state):
        result = await handle_durak_message(from_state)
        assert json.loads(result) == json.loads(to_state)
        mocked_persist.assert_called_once()

    return wrapped


@pytest.fixture
def assert_snapshot_matches(assert_handle_message, snapshot):
    async def wrapped(input_path):
        with open(input_path, "r") as f:
            actual = await handle_durak_message(f.read())
            snapshot.assert_match(actual)

    return wrapped


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_path", SCENARIO_INPUT_FILES, ids=lambda p: os.path.split(p)[1]
)
async def test_scenarios(input_path, assert_snapshot_matches):
    await assert_snapshot_matches(input_path)


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
