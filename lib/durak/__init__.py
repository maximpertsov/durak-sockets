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


def start_game(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.draw()
    return game.serialize()


def organize_cards(*, from_state, user, payload):
    game = Game.deserialize(from_state)
    game.organize_cards(player=user, **payload)
    return game.serialize()
