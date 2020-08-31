from functools import reduce


class Player:
    HAND_SIZE = 6

    def __init__(self, *, name, cards, order, yielded=False):
        self.name = name
        self._cards = cards
        self.order = order
        self.yielded = yielded

    def serialize(self):
        return {
            "name": self.name,
            "cards": self._cards,
            "order": self.order,
            "yielded": self.yielded,
        }

    def card_count(self):
        return sum(1 for card in self._cards if card)

    def in_game(self):
        return bool(self._cards)

    def take_cards(self, *, cards):
        # TODO: maybe compacting should happen client-side?
        self._compact_hand()
        self._cards += cards

    def remove_card(self, *, card):
        self._cards = [
            None if hand_card == card else hand_card for hand_card in self._cards
        ]

    def draw(self, *, draw_pile):
        draw_count = max(self.HAND_SIZE - self.card_count(), 0)
        self.take_cards(cards=draw_pile.draw(count=draw_count))
        # TODO: maybe compacting should happen client-side?
        self._compact_hand()

    def _compact_hand(self):
        self._cards = self.cards()

    def cards(self):
        return [card for card in self._cards if card]


class DrawPile:
    def __init__(self, *, draw_pile):
        self._draw_pile = draw_pile

    def serialize(self):
        return self._draw_pile

    def size(self):
        return len(self._draw_pile)

    def draw(self, count):
        result = self._draw_pile[:count]
        self._draw_pile = self._draw_pile[count:]
        return result


from lib.durak.game import Game


def attack(*, from_state, user, payload):
    game = Game.deserialize(**from_state)
    game.attack(player=user, **payload)
    return game.serialize()


def attack_with_many(*, from_state, user, payload):
    def step(state, card):
        return attack(from_state=state, user=user, payload={"card": card})

    return reduce(step, payload["cards"], from_state)


def defend(*, from_state, user, payload):
    game = Game.deserialize(**from_state)
    game.defend(player=user, **payload)
    return game.serialize()


def yield_attack(*, from_state, user, payload):
    game = Game.deserialize(**from_state)
    game.yield_attack(player=user, **payload)
    return game.serialize()


def collect(*, from_state, user, payload):
    game = Game.deserialize(**from_state)
    game.collect(player=user, **payload)
    return game.serialize()


def pass_card(*, from_state, user, payload):
    game = Game.deserialize(**from_state)
    game.pass_cards(player=user, cards=[payload["card"]])
    return game.serialize()


def pass_with_many(*, from_state, user, payload):
    game = Game.deserialize(**from_state)
    game.pass_cards(player=user, **payload)
    return game.serialize()


def start_game(*, from_state, user, payload):
    game = Game.deserialize(**from_state)
    game.draw()
    return game.serialize()
