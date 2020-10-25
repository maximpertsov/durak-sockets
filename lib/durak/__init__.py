import json
from copy import deepcopy
from enum import Enum
from os import environ

import httpx
from lib.durak.exceptions import IllegalAction, ActionNotDefined
from lib.durak.game import Game


def noop(*, from_state):
    return Game.deserialize(from_state).serialize()


def attack(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.attack(player=user, cards=[payload["card"]])
    return game.serialize()


def attack_with_many(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.attack(player=user, **payload)
    return game.serialize()


def defend(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.defend(player=user, **payload)
    return game.serialize()


def yield_attack(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.yield_attack(player=user, **payload)
    return game.serialize()


def give_up(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.give_up(player=user)
    return game.serialize()


def pass_card(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.pass_cards(player=user, cards=[payload["card"]])
    return game.serialize()


def pass_with_many(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.pass_cards(player=user, **payload)
    return game.serialize()


def join_game(*, from_state, user, payload):
    state = deepcopy(from_state)

    joined = set(state.get("joined", [])) | set([user])
    player_ids = [
        player["id"] if isinstance(player, dict) else player
        for player in state["players"]
    ]
    if joined != set(player_ids):
        state.update(joined=joined)
        return state

    players = [
        {"id": player["id"] if isinstance(player, dict) else player, "hand": []}
        for player in state["players"]
    ]

    state.update(
        players=players,
        collector=None,
        drawn_cards=[],
        durak=None,
        pass_count=0,
        table=[],
        yielded=[],
    )

    game = Game.deserialize(state)
    game.draw()
    return game.serialize()


def organize_cards(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.organize_cards(player=user, **payload)
    return game.serialize()


actions = {
    "joined_game": join_game,
    "attacked": attack,
    "attacked_with_many": attack_with_many,
    "defended": defend,
    "gave_up": give_up,
    "organized": organize_cards,
    "passed": pass_card,
    "passed_with_many": pass_with_many,
    "yielded_attack": yield_attack,
}


class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, set):
            return sorted(obj)
        return json.JSONEncoder.default(self, obj)


async def handle_message(message, config=None):
    data = json.loads(message)

    try:
        try:
            action = actions[data["type"]]
        except KeyError:
            raise ActionNotDefined
        data["to_state"] = action(
            from_state=data["from_state"], user=data["user"], payload=data["payload"]
        )
        await persist(data)
    except IllegalAction:
        data["to_state"] = noop(from_state=data["from_state"])
        data["no_display"] = True
    except ActionNotDefined:
        data["to_state"] = deepcopy(data["from_state"])
        data["no_display"] = True

    del data["from_state"]

    # TODO: generalize non-displayable actions?
    if data["type"] == "organized":
        data["no_display"] = True

    return json.dumps(data, cls=MessageEncoder)


BASE_API_URL = environ.get("BASE_API_URL", "http://localhost:8000/api")
SCHEMA_VERSION = 2


async def persist(data):
    async with httpx.AsyncClient() as client:
        await client.post(
            "{}/game/{}/events".format(BASE_API_URL, data["game"]),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"version": SCHEMA_VERSION, **data}, cls=MessageEncoder),
        )
