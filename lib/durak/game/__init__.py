from collections import deque

from lib.durak.draw_pile import DrawPile
from lib.durak.exceptions import IllegalAction
from lib.durak.status import Status
from lib.durak.table import Table

from .collector import Collector
from .legal_attacks import LegalAttacks
from .players import Players
from .queries import LegalDefenses, LegalPasses
from .yielded import Yielded


class Game:
    class DifferentRanks(IllegalAction):
        pass

    class IllegalAttack(IllegalAction):
        pass

    @classmethod
    def deserialize(cls, state):
        return cls(
            draw_pile=DrawPile(
                drawn_cards=state["drawn_cards"],
                seed=state["seed"],
                lowest_rank=state["lowest_rank"],
            ),
            players=Players.deserialize(state["players"]),
            table=Table(table=state["table"]),
            state=state,
        )

    def __init__(self, *, draw_pile, players, table, state):
        self._draw_pile = draw_pile
        self._players = players
        self._table = table

        self._pass_count = state["pass_count"]
        self._lowest_rank = state["lowest_rank"]
        self._attack_limit = state["attack_limit"]
        self._with_passing = state["with_passing"]

        self._collector = Collector(game=self)
        self._yielded = Yielded(game=self)

        self._legal_attacks = LegalAttacks(game=self)

    def serialize(self):
        return {
            "attackers": [player.id for player in self._attackers()],
            "defender": getattr(self._defender(), "id", None),
            "legal_attacks": self._legal_attacks.serialize(),
            "legal_defenses": LegalDefenses.result(game=self),
            "legal_passes": LegalPasses.result(game=self),
            "table": self._table.serialize(),
            "pass_count": self._pass_count,
            "players": self._serialize_players(),
            "trump_suit": self._trump_suit,
            "winners": set(player.id for player in self.winners()),
            "lowest_rank": self._lowest_rank,
            "attack_limit": self._attack_limit,
            "with_passing": self._with_passing,
            **self._draw_pile.serialize(),
        }

    def _serialize_players(self):
        for player in self.ordered_players():
            if self._durak == player:
                player.add_status(Status.DURAK)
        return self._players.serialize()

    @property
    def _trump_suit(self):
        return self._draw_pile.trump_suit

    def winners(self):
        return set(self.ordered_players()) - set(self._active_players())

    @property
    def _durak(self):
        if len(self._active_players()) == 1:
            return self._active_players()[0]

    def _attack(self, *, player, card):
        self.player(player).remove_card(card=card)
        self._table.add_card(card=card)

    def attack(self, *, player, cards):
        for card in cards:
            self._attack(player=player, card=card)
        self._clear_yields()

    def legally_attack(self, *, player, cards):
        self._legal_attacks.validate(player=player, cards=cards)
        self.attack(player=player, cards=cards)

    def defend(self, *, player, base_card, card):
        self.player(player).remove_card(card=card)
        self._table.stack_card(base_card=base_card, card=card)
        self._clear_yields()

    def yield_attack(self, *, player):
        self._yielded.add(player=player)
        if not self._no_more_attacks():
            return

        if self._collector:
            self.collect()
            return

        self._successful_defense_cleanup()

    def collect(self):
        self._collector.get().take_cards(cards=self._table.collect())
        self.draw()
        self._rotate(skip=1)
        self._collector.clear()
        self._clear_yields()
        self._compact_hands()

    def _successful_defense_cleanup(self):
        self._table.clear()
        self.draw()
        self._rotate()
        self._clear_yields()
        self._compact_hands()

    def draw(self):
        players = deque(self._ordered_players_with_cards_in_round())
        players.rotate(self._pass_count)
        for index, player in enumerate(players):
            player.draw(draw_pile=self._draw_pile)
        self._pass_count = 0

    def _pass_card(self, *, player, card):
        self.player(player).remove_card(card=card)
        self._table.add_card(card=card)

    def pass_cards(self, *, player, cards):
        for card in cards:
            self._pass_card(player=player, card=card)
        self._pass_count += 1
        self._clear_yields()
        self._rotate()

    def give_up(self, *, player):
        self._collector.set(player=player)
        self._clear_yields()

    def organize_cards(self, *, player, strategy):
        self.player(player).organize_cards(
            strategy=strategy, trump_suit=self._trump_suit
        )

    def _rotate(self, *, skip=0):
        players = deque(self._ordered_players_with_cards_in_round())
        players.rotate(-1 - skip)

        for index, player in enumerate(players):
            player.order = index

    def _compact_hands(self):
        for player in self._ordered_players_with_cards_in_round():
            player.compact_hand()

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

    def _no_more_attacks(self):
        return set(self._attackers()).issubset(self._yielded_players())

    def _yielded_players(self):
        return self._yielded.get()

    def _clear_yields(self):
        self._yielded.clear()

    def _active_players(self):
        return [
            player
            for player in self.ordered_players()
            if self._draw_pile.size() or player.cards()
        ]

    def _ordered_players_with_cards_in_round(self):
        return [
            player
            for player in self.ordered_players()
            if player.had_cards_in_round() or self._draw_pile.size()
        ]

    def ordered_players(self):
        return self._players.ordered()

    def player(self, player_or_id):
        return self._players.player(player_or_id)
