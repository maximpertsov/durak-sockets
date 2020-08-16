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


class Hands:
    def __init__(self, hands):
        self._hands = {
            player: [Card(card=card) for card in cards]
            for player, cards in hands.items()
        }

    def serialize(self):
        return {
            player: [card.serialize() for card in cards]
            for player, cards in self._hands.items()
        }

    def take_cards(self, *, player, cards):
        card_objects = [Card(card=card) for card in cards]
        # TODO: maybe compacting should happen client-side?
        compact_hand = [
            _card for _card in self._player_hand(player) if not _card.is_empty_space()
        ]
        self._hands.update({player: compact_hand + card_objects})

    def remove_card(self, *, player, card):
        card_object = Card(card=card)
        self._hands.update(
            {
                player: [
                    Card(card=None) if _card == card_object else _card
                    for _card in self._player_hand(player)
                ]
            }
        )

    def _player_hand(self, player):
        return self._hands[player]


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
        result = self._draw_pile[:count]
        self._draw_pile = self._draw_pile[count:]
        return result


class Game:
    def __init__(self, *, draw_pile, players, hands, table, yielded):
        self._draw_pile = DrawPile(draw_pile=draw_pile)
        self._hands = Hands(hands=hands)
        self._table = Table(table=table)
        self._players = players
        self._yielded = set(yielded)

    def serialize(self):
        return {
            "draw_pile": self._draw_pile.serialize(),
            "hands": self._hands.serialize(),
            "table": self._table.serialize(),
            "players": self._players,
            "yielded": list(self._yielded),
        }

    def attack(self, *, player, card):
        self._hands.remove_card(player=player, card=card)
        self._table.add_card(card=card)
        self._yielded.clear()

    def defend(self, *, player, base_card, card):
        self._hands.remove_card(player=player, card=card)
        self._table.stack_card(base_card=base_card, card=card)
        self._yielded.clear()

    def yield_attack(self, *, player):
        self._yielded.add(player)
        raise NotImplementedError("Draw routine after all attackers have yielded")


def attack(*, from_state, user, payload):
    game = Game(**from_state)
    game.attack(player=user, **payload)
    return game.serialize()


def defend(*, from_state, user, payload):
    game = Game(**from_state)
    game.defend(player=user, **payload)
    return game.serialize()
