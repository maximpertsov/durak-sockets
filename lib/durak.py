class Card:
    def __init__(self, *, card):
        if not card:
            self.rank = None
            self.suit = None
        else:
            self.rank = card["rank"]
            self.suit = card["suit"]

    def serialize(self):
        return {"rank": self.rank, "suit": self.suit}

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

    def remove_card(self, *, player, card):
        card_object = Card(card=card)
        self._hands.update(
            {
                player: [
                    _card for _card in self._player_hand(player) if _card != card_object
                ]
            }
        )
        return self

    def _player_hand(self, player):
        return self._hands[player]


class Table:
    def __init__(self, table):
        self._table = [[Card(card=card) for card in cards] for cards in table]

    def serialize(self):
        return [[card.serialize() for card in cards] for cards in self._table]

    def add_card(self, *, card):
        self._table.append([Card(card=card)])
        return self


def attack(*, user, card, hands, table, **kwargs):
    return {
        "hands": Hands(hands=hands).remove_card(player=user, card=card).serialize(),
        "table": Table(table=table).add_card(card=card).serialize(),
        "yielded": [],
    }
