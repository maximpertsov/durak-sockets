from operator import attrgetter


class Card:
    def __init__(self, *, card):
        if not card:
            self.rank = None
            self.suit = None
        else:
            self.rank = card["rank"]
            self.suit = card["suit"]

    def serialize(self):
        if self.is_empty_space():
            return None
        return {"rank": self.rank, "suit": self.suit}

    def is_empty_space(self):
        return self.rank is None and self.suit is None

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __repr__(self):
        return repr(self.serialize())

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Player:
    HAND_SIZE = 6

    def __init__(self, *, name, cards, order, yielded=False):
        self.name = name
        self._cards = [Card(card=card) for card in cards]
        self.order = order
        self.yielded = yielded

    def serialize(self):
        return {
            "name": self.name,
            "cards": [card.serialize() for card in self._cards],
            "order": self.order,
            "yielded": self.yielded,
        }

    def card_count(self):
        return sum(1 for card in self._cards if not card.is_empty_space())

    def take_cards(self, *, cards):
        card_objects = [Card(card=card) for card in cards]
        # TODO: maybe compacting should happen client-side?
        self._compact_hand()
        self._cards += card_objects

    def remove_card(self, *, card):
        card_object = Card(card=card)
        self._cards = [
            Card(card=None) if _card == card_object else _card for _card in self._cards
        ]

    def draw(self, *, draw_pile):
        draw_count = max(self.HAND_SIZE - self.card_count(), 0)
        self.take_cards(cards=draw_pile.draw(count=draw_count))
        # TODO: maybe compacting should happen client-side?
        self._compact_hand()

    def _compact_hand(self):
        self._cards = [card for card in self._cards if not card.is_empty_space()]


class Table:
    class BaseCardNotFound(Exception):
        pass

    def __init__(self, table):
        self._table = [[Card(card=card) for card in cards] for cards in table]

    def serialize(self):
        return [[card.serialize() for card in cards] for cards in self._table]

    def add_card(self, *, card):
        self._table.append([Card(card=card)])

    def stack_card(self, *, base_card, card):
        base_card_object = Card(card=base_card)

        for cards in self._table:
            if cards[-1] == base_card_object:
                cards.append(Card(card=card))
                return
        else:
            raise self.BaseCardNotFound


class DrawPile:
    def __init__(self, *, draw_pile):
        self._draw_pile = [Card(card=card) for card in draw_pile]

    def serialize(self):
        return [card.serialize() for card in self._draw_pile]

    def size(self):
        return len(self._draw_pile)

    def draw(self, count):
        result = [card.serialize() for card in self._draw_pile[:count]]
        self._draw_pile = self._draw_pile[count:]
        return result


class Game:
    @classmethod
    def deserialize(cls, *, draw_pile, players, hands, table, yielded):
        return cls(
            draw_pile=DrawPile(draw_pile=draw_pile),
            players={
                player: Player(name=player, cards=hands[player], order=order)
                for order, player in enumerate(players)
            },
            table=Table(table=table),
        )

    def __init__(self, *, draw_pile, players, table):
        self._draw_pile = draw_pile
        self._players = players
        self._table = table

    def serialize(self):
        return {
            "draw_pile": self._draw_pile.serialize(),
            "hands": {
                serialized["name"]: serialized["cards"]
                for serialized in [
                    player.serialize() for player in self._players.values()
                ]
            },
            "table": self._table.serialize(),
            "players": [
                player.name
                for player in sorted(self._players.values(), key=attrgetter("order"))
            ],
            "yielded": [
                player.name for player in self._players.values() if player.yielded
            ],
        }

    def attack(self, *, player, card):
        self._get_player(player).remove_card(card=card)
        self._table.add_card(card=card)
        for _player in self._players.values():
            _player.yielded = False

    def defend(self, *, player, base_card, card):
        self._get_player(player).remove_card(card=card)
        self._table.stack_card(base_card=base_card, card=card)
        for _player in self._players.values():
            _player.yielded = False

    def yield_attack(self, *, player):
        raise NotImplementedError("Draw routine after all attackers have yielded")

    def _get_player(self, player):
        return self._players[player]


def attack(*, from_state, user, payload):
    game = Game.deserialize(**from_state)
    game.attack(player=user, **payload)
    return game.serialize()


def defend(*, from_state, user, payload):
    game = Game.deserialize(**from_state)
    game.defend(player=user, **payload)
    return game.serialize()
