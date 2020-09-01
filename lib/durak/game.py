from functools import lru_cache
from itertools import chain
from operator import attrgetter

from lib.durak import DrawPile, Player
from lib.durak.table import Table


class Game:
    @classmethod
    def deserialize(
        cls, *, draw_pile, hands, pass_count, players, table, trump_suit, yielded
    ):
        return cls(
            draw_pile=DrawPile(draw_pile=draw_pile),
            players={
                player: Player(
                    name=player,
                    cards=hands[player],
                    order=order,
                    yielded=player in yielded,
                )
                for order, player in enumerate(players)
            },
            pass_count=pass_count,
            table=Table(table=table),
            trump_suit=trump_suit,
        )

    def __init__(self, *, draw_pile, pass_count, players, table, trump_suit):
        self._draw_pile = draw_pile
        self._pass_count = pass_count
        self._players = players
        self._table = table
        self._trump_suit = trump_suit

    def serialize(self):
        return {
            "draw_pile": self._draw_pile.serialize(),
            "hands": {
                serialized["name"]: serialized["cards"]
                for serialized in [
                    player.serialize() for player in self._players.values()
                ]
            },
            "legal_attacks": self.legal_attacks(),
            "legal_defenses": self.legal_defenses(),
            "table": self._table.serialize(),
            "pass_count": self._pass_count,
            "players": [
                player.name for player in self._ordered_players() if player.in_game()
            ],
            "trump_suit": self._trump_suit,
            "yielded": [player.name for player in self._yielded_players()],
        }

    def legal_attacks(self):
        if self._defender() is None:
            return set([])
        if len(self._defender().cards()) <= len(self._table.undefended_cards()):
            return set([])

        attacker_cards = set(
            chain.from_iterable(player.cards() for player in self._attackers())
        )

        return attacker_cards & self._table.legal_attacks()

    def legal_defenses(self):
        if self._defender() is None:
            return {}

        defender_cards = set(self._defender().cards())
        return {
            base_card: defender_cards & cards
            for base_card, cards in self._table.legal_defenses(
                trump_suit=self._trump_suit
            ).items()
        }

    def attack(self, *, player, card):
        self._player(player).remove_card(card=card)
        self._table.add_card(card=card)
        self._clear_yields()

    def defend(self, *, player, base_card, card):
        self._player(player).remove_card(card=card)
        self._table.stack_card(base_card=base_card, card=card)
        self._clear_yields()

    def draw(self):
        player_count = len(self._ordered_players())
        for index in range(player_count):
            index_with_passes = (index - self._pass_count) % player_count
            player = self._ordered_players()[index_with_passes]
            player.draw(draw_pile=self._draw_pile)
        self._pass_count = 0

    def collect(self, *, player):
        self._player(player).take_cards(cards=self._table.collect())
        self.draw()
        self._rotate(skip=1)
        self._clear_yields()

    def yield_attack(self, *, player):
        self._player(player).yielded = True
        if self._no_more_attacks():
            self._table.clear()
            self.draw()
            self._rotate()
            self._clear_yields()

    def _pass_card(self, *, player, card):
        self._player(player).remove_card(card=card)
        self._table.add_card(card=card)

    def pass_cards(self, *, player, cards):
        for card in cards:
            self._pass_card(player=player, card=card)
        self._pass_count += 1
        self._clear_yields()
        self._rotate()

    def _rotate(self, *, skip=0):
        shift = skip + 1
        players = self._ordered_players()[shift:] + self._ordered_players()[:shift]
        for order, player in enumerate(players):
            player.order = order
        self._ordered_players.cache_clear()

    def _player(self, player):
        return self._players[player]

    @lru_cache
    def _ordered_players(self):
        return sorted(self._players.values(), key=attrgetter("order"))

    def _defender(self):
        if len(self._ordered_players()) < 2:
            return
        return self._ordered_players()[1]

    def _attackers(self):
        if not self._ordered_players():
            return []
        if len(self._ordered_players()) == 1 or not self._table.cards():
            return self._ordered_players()[:1]

        return [
            player for player in self._ordered_players() if player != self._defender()
        ]

    def _no_more_attacks(self):
        not_yielded = set(self._players.values()).difference(
            set(self._yielded_players())
        )
        return not_yielded == set([self._defender()])

    def _yielded_players(self):
        return [player for player in self._players.values() if player.yielded]

    def _clear_yields(self):
        for _player in self._players.values():
            _player.yielded = False
