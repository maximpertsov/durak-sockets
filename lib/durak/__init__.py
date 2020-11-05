import json
from copy import deepcopy
from enum import Enum
from os import environ

import httpx
from lib.durak.exceptions import ActionNotDefined, IllegalAction
from lib.durak.game import AI, Game


def noop(*, from_state):
    return Game.deserialize(from_state).serialize()


def attack(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.legally_attack(player=user, **payload)
    return game.serialize()


def defend(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.legally_defend(player=user, **payload)
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
    game.legally_pass_cards(player=user, **payload)
    return game.serialize()


def join_game(*, from_state, user, payload):
    state = deepcopy(from_state)

    joined = set(state.get("joined", [])) | set([user])
    players = state["players"]

    if joined != set(player["id"] for player in players):
        state.update(joined=joined)
        return state

    for index, player in enumerate(players):
        player.setdefault("hand", [])
        player.setdefault("order", index)
        player.setdefault("state", [])

    state.update(
        players=players,
        drawn_cards=[],
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


def auto_action(*, from_state, user, payload):
    """
    Game will select an action for the user to perform.
    It is assumed that the "user" is a bot.
    """
    for _ in range(100):
        try:
            game = Game.deserialize(from_state)
            action_type = game.auto_action(player=user, **payload)
            print(f"{user} {action_type}")
            return game.serialize()
        except AI.CannotPerform:
            pass
    else:
        raise IllegalAction


actions = {
    "joined_game": join_game,
    "polled_for_action": auto_action,
    "attacked": attack,
    "defended": defend,
    "gave_up": give_up,
    "organized": organize_cards,
    "passed": pass_card,
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
SCHEMA_VERSION = 3


async def persist(data):
    async with httpx.AsyncClient() as client:
        await client.post(
            "{}/game/{}/events".format(BASE_API_URL, data["game"]),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"version": SCHEMA_VERSION, **data}, cls=MessageEncoder),
        )
