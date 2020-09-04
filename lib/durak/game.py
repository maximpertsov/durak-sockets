from itertools import chain
from operator import attrgetter

from lib.durak.draw_pile import DrawPile
from lib.durak.player import Player
from lib.durak.table import Table


class Game:
    @classmethod
    def deserialize(
        cls,
        *,
        draw_pile,
        hands,
        pass_count,
        players,
        table,
        trump_suit,
        yielded,
        lowest_rank,
        with_passing,
        attack_limit
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
            lowest_rank=lowest_rank,
            with_passing=with_passing,
            attack_limit=attack_limit,
        )

    def __init__(
        self,
        *,
        draw_pile,
        pass_count,
        players,
        table,
        trump_suit,
        lowest_rank,
        with_passing,
        attack_limit
    ):
        self._draw_pile = draw_pile
        self._pass_count = pass_count
        self._players = players
        self._table = table
        self._trump_suit = trump_suit
        self._lowest_rank = lowest_rank
        self._attack_limit = attack_limit
        self._with_passing = with_passing

    def serialize(self):
        return {
            "attackers": [player.name for player in self._attackers()],
            "defender": getattr(self._defender(), "name", None),
            "draw_pile": self._draw_pile.serialize(),
            "durak": getattr(self.durak(), "name", None),
            "hands": {
                serialized["name"]: serialized["cards"]
                for serialized in [
                    player.serialize() for player in self._ordered_players()
                ]
            },
            "legal_attacks": self.legal_attacks(),
            "legal_defenses": self.legal_defenses(),
            "legal_passes": self.legal_passes(),
            "table": self._table.serialize(),
            "pass_count": self._pass_count,
            "players": [player.name for player in self._ordered_players()],
            "trump_suit": self._trump_suit,
            "winners": set(player.name for player in self.winners()),
            "yielded": [player.name for player in self._yielded_players()],
            "lowest_rank": self._lowest_rank,
            "attack_limit": self._attack_limit,
            "with_passing": self._with_passing,
        }

    def winners(self):
        return set(self._ordered_players()) - set(self._active_players())

    def durak(self):
        if len(self._active_players()) == 1:
            return self._active_players()[0]

    def legal_attacks(self):
        if self._defender() is None:
            return {"cards": set([]), "limit": 0}

        limit = max(
            0, len(self._defender().cards()) - len(self._table.undefended_cards())
        )
        attacker_cards = set(
            chain.from_iterable(player.cards() for player in self._attackers())
        )
        return {
            "cards": attacker_cards & self._table.legal_attacks(),
            "limit": limit,
        }

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

    def legal_passes(self):
        if self._pass_recipient() is None:
            return {"cards": set([]), "limit": 0}

        limit = max(
            0, len(self._pass_recipient().cards()) - len(self._table.undefended_cards())
        )
        defender_cards = set(self._defender().cards())
        return {
            "cards": defender_cards & self._table.legal_passes(),
            "limit": limit,
        }

    def _attack(self, *, player, card):
        self._player(player).remove_card(card=card)
        self._table.add_card(card=card)

    def attack(self, *, player, cards):
        for card in cards:
            self._attack(player=player, card=card)
        self._clear_yields()

    def defend(self, *, player, base_card, card):
        self._player(player).remove_card(card=card)
        self._table.stack_card(base_card=base_card, card=card)
        self._clear_yields()

    def draw(self):
        players = self._ordered_players_with_cards_in_round()
        player_count = len(players)
        for index in range(player_count):
            index_with_passes = (index - self._pass_count) % player_count
            player = players[index_with_passes]
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
        players = self._ordered_players()
        shift = skip + 1
        for index, player in enumerate(players):
            player.order = (index - shift) % len(players)

    def _player(self, player):
        return self._players[player]

    def _defender(self):
        players = self._ordered_players_with_cards_in_round()
        if len(players) < 2:
            return
        return players[1]

    def _attackers(self):
        players = self._ordered_players_with_cards_in_round()
        if not players:
            return []

        potential_attackers = [
            player
            for player in players
            if player != self._defender() and player.cards()
        ]

        return potential_attackers if self._table.cards() else potential_attackers[:1]

    def _pass_recipient(self):
        if not self._defender():
            return

        players = self._ordered_players_with_cards_in_round()
        players_from_defender = players[2:] + [players[0]]
        next_players_with_cards = [
            player for player in players_from_defender if player.cards()
        ]
        if not next_players_with_cards:
            return
        return next_players_with_cards[0]

    def _no_more_attacks(self):
        not_yielded = set(self._active_players()).difference(
            set(self._yielded_players())
        )
        return not_yielded == set([self._defender()])

    def _yielded_players(self):
        return [player for player in self._active_players() if player.yielded]

    def _clear_yields(self):
        for _player in self._active_players():
            _player.yielded = False

    def _active_players(self):
        return [
            player
            for player in self._ordered_players()
            if self._draw_pile.size() or player.cards()
        ]

    def _ordered_players_with_cards_in_round(self):
        return [
            player for player in self._ordered_players() if player.had_cards_in_round()
        ]

    def _ordered_players(self):
        return sorted(self._players.values(), key=attrgetter("order"))
