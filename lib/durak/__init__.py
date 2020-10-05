from copy import deepcopy

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


# TODO: change to "join" game
def start_game(*, from_state, user, payload):
    state = deepcopy(from_state)

    joined = set(state.get('joined', [])) | set([user])
    if joined != set(state['players']):
        state.update(joined=joined)
        return state

    state.update(
        collector=None,
        drawn_cards=[],
        durak=None,
        hands={player: [] for player in from_state["players"]},
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
