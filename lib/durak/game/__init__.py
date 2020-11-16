from collections import deque

from lib.durak.draw_pile import DrawPile
from lib.durak.status import Status
from lib.durak.table import Table

from .ai import AI
from .collector import Collector
from .legal_attacks import LegalAttacks
from .legal_defenses import LegalDefenses
from .legal_passes import LegalPasses
from .players import Players
from .yielded import Yielded


class Game:
    @classmethod
    def deserialize(cls, state):
        return cls(
            draw_pile=DrawPile(
                drawn_cards=state["drawn_cards"],
                seed=state["seed"],
                lowest_rank=state["lowest_rank"],
            ),
            players=Players.deserialize(state["players"]),
            state=state,
        )

    def __init__(self, *, draw_pile, players, state):
        self._draw_pile = draw_pile
        self._players = players

        self._pass_count = state["pass_count"]
        self._lowest_rank = state["lowest_rank"]
        self._attack_limit = state["attack_limit"]
        self._with_passing = state["with_passing"]

        self._table = Table(game=self)
        self._collector = Collector(game=self)
        self._yielded = Yielded(game=self)

        self._legal_attacks = LegalAttacks(game=self)
        self.legal_defenses = LegalDefenses(game=self)
        self._legal_passes = LegalPasses(game=self)

        self._ai = AI(game=self)

    def serialize(self):
        return {
            "attackers": [player.id for player in self.attackers],
            "defender": getattr(self.defender, "id", None),
            "legal_attacks": self._legal_attacks.serialize(),
            "legal_defenses": self.legal_defenses.serialize(),
            "legal_passes": self._legal_passes.serialize(),
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
            player.organize_cards(trump_suit=self._trump_suit)
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
        self._table.attack(player=self.player(player), card=card)

    def attack(self, *, player, cards):
        for card in cards:
            self._attack(player=player, card=card)
        self._clear_yields()

    def legally_attack(self, *, player, cards):
        self._legal_attacks.validate(player=player, cards=cards)
        self.attack(player=player, cards=cards)

    def defend(self, *, player, base_card, card):
        self._table.defend(
            player=self.player(player),
            attack_card=base_card,
            defense_card=card,
        )
        self._clear_yields()

    def legally_defend(self, *, player, base_card, card):
        self.legal_defenses.validate(player=player, base_card=base_card, card=card)
        self.defend(player=player, base_card=base_card, card=card)

    def yield_attack(self, *, player):
        self._yielded.add(player=player)

        if not self._no_more_attacks():
            return

        if self._collector:
            self.collect()
            return

        if self._table.undefended_cards() and self.defender.cards():
            return

        self._successful_defense_cleanup()

    def collect(self):
        self._table.collect(player=self._collector.get())
        self.draw()
        self._rotate(skip=1)
        self._collector.clear()
        self._clear_yields()
        self._remove_players()

    def _successful_defense_cleanup(self):
        self._table.return_undefended()
        self.draw()
        self._rotate()
        self._clear_yields()
        self._remove_players()

    def _remove_players(self):
        for player in self._ordered_players_with_cards_in_round():
            if not player.cards():
                player.remove_from_game()

    def draw(self):
        players = deque(self._ordered_players_with_cards_in_round())
        players.rotate(self._pass_count)
        for player in players:
            player.draw(draw_pile=self._draw_pile)
        self._pass_count = 0

    def _pass_card(self, *, player, card):
        self._table.attack(player=self.player(player), card=card)

    def pass_cards(self, *, player, cards):
        for card in cards:
            self._pass_card(player=player, card=card)
        self._pass_count += 1
        self._clear_yields()
        self._rotate()

    def legally_pass_cards(self, *, player, cards):
        self._legal_passes.validate(player=player, cards=cards)
        self.pass_cards(player=player, cards=cards)

    def give_up(self, *, player):
        self._collector.set(player=player)
        self._clear_yields()

    def organize_cards(self, *, player, strategy):
        self.player(player).update_organize_strategy(
            strategy=strategy, trump_suit=self._trump_suit
        )

    def auto_action(self, *, player):
        return self._ai.perform_action(player=player)

    def _rotate(self, *, skip=0):
        players = deque(self._ordered_players_with_cards_in_round())
        players.rotate(-1 - skip)

        for index, player in enumerate(players):
            player.order = index

    @property
    def defender(self):
        players = self._ordered_players_with_cards_in_round()
        if len(players) < 2:
            return
        return players[1]

    @property
    def attackers(self):
        players = self._ordered_players_with_cards_in_round()
        if not players:
            return []

        potential_attackers = [
            player for player in players if player != self.defender and player.cards()
        ]

        return potential_attackers if self._table.cards() else potential_attackers[:1]

    def _no_more_attacks(self):
        return set(self.attackers).issubset(self._yielded_players())

    def _yielded_players(self):
        return self._yielded.get()

    def _clear_yields(self):
        self._yielded.clear()

    def _active_players(self):
        return [
            player
            for player in self.ordered_players()
            # TODO: confirm that there are no undefended cards to take back in undefended
            # mode
            if self._draw_pile.size() or player.cards()
        ]

    def _ordered_players_with_cards_in_round(self):
        return [
            player
            for player in self.ordered_players()
            if not player.has_status(Status.OUT_OF_PLAY)
        ]

    def ordered_players(self):
        return self._players.ordered()

    def player(self, player_or_id):
        return self._players.player(player_or_id)
