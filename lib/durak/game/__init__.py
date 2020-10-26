from enum import Enum
from operator import attrgetter

from lib.durak.card import get_rank
from lib.durak.draw_pile import DrawPile
from lib.durak.exceptions import IllegalAction
from lib.durak.player import Player
from lib.durak.table import Table

from .queries import LegalAttacks, LegalDefenses, LegalPasses


class Status(Enum):
    COLLECTING = "collecting"
    DURAK = "durak"
    YIELDED = "yielded"


# TODO: remove this helper after player schema update is finished
def get_player_id(state, player):
    return player["id"] if isinstance(player, dict) else player


# TODO: remove this helper after player schema update is finished
def get_hand(state, player):
    try:
        return player["hand"] if isinstance(player, dict) else state["hands"][player]
    except KeyError:
        return state["hands"][player["id"]]


# TODO: remove this helper after player schema update is finished
def is_yielded(state, player):
    try:
        return (
            "yielded" in player["state"]
            if isinstance(player, dict)
            else player in state["yielded"]
        )
    except KeyError:
        return player["id"] in state["yielded"]


# TODO: remove this helper after player schema update is finished
def get_collector(state):
    for player in state["players"]:
        try:
            if Status.COLLECTING.value in player["state"]:
                return player["id"]
        except KeyError:
            return None
        except TypeError:
            return state["collector"]


# TODO: remove this helper after player schema update is finished
def get_durak(state):
    for player in state["players"]:
        try:
            if Status.DURAK.value in player["state"]:
                return player["id"]
        except KeyError:
            return None
        except TypeError:
            return state["durak"]


class Game:
    class MultipleCollectors(IllegalAction):
        pass

    class DifferentRanks(IllegalAction):
        pass

    @classmethod
    def deserialize(cls, state):
        return cls(
            draw_pile=DrawPile(
                drawn_cards=state["drawn_cards"],
                seed=state["seed"],
                lowest_rank=state["lowest_rank"],
            ),
            players={
                get_player_id(state, player): Player(
                    name=get_player_id(state, player),
                    cards=get_hand(state, player),
                    order=(
                        (player.get("order") or order)
                        if isinstance(player, dict)
                        else order
                    ),
                    state=[Status.YIELDED] if is_yielded(state, player) else [],
                )
                for order, player in enumerate(state["players"])
            },
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

        # TODO: remove this helper helpers after player schema update is finished
        if durak := get_durak(state):
            self._player(durak).add_status(Status.DURAK)

        # TODO: remove this helper helpers after player schema update is finished
        if collector := get_collector(state):
            self._player(collector).add_status(Status.COLLECTING)

    def serialize(self):
        return {
            "attackers": [player.name for player in self._attackers()],
            "defender": getattr(self._defender(), "name", None),
            "legal_attacks": LegalAttacks.result(game=self),
            "legal_defenses": LegalDefenses.result(game=self),
            "legal_passes": LegalPasses.result(game=self),
            "table": self._table.serialize(),
            "pass_count": self._pass_count,
            "players": self._serialize_players(),
            "trump_suit": self._trump_suit,
            "winners": set(player.name for player in self.winners()),
            "lowest_rank": self._lowest_rank,
            "attack_limit": self._attack_limit,
            "with_passing": self._with_passing,
            **self._draw_pile.serialize(),
        }

    def _serialize_players(self):
        result = []
        for player in self._ordered_players():
            if self._durak == player:
                player.add_status(Status.DURAK)
            result.append(player.serialize())
        return result

    @property
    def _trump_suit(self):
        return self._draw_pile.trump_suit

    # TODO: cache?
    @property
    def _collector(self):
        result = None

        for player in self._ordered_players():
            if not player.has_status(Status.COLLECTING):
                continue
            if result is not None:
                raise self.MultipleCollectors

            result = player

        return result

    def winners(self):
        return set(self._ordered_players()) - set(self._active_players())

    @property
    def _durak(self):
        if len(self._active_players()) == 1:
            return self._active_players()[0]

    def _attack(self, *, player, card):
        self._player(player).remove_card(card=card)
        self._table.add_card(card=card)

    def attack(self, *, player, cards):
        if len(set(get_rank(card) for card in cards)) > 1:
            raise self.DifferentRanks

        for card in cards:
            self._attack(player=player, card=card)
        self._clear_yields()

    def defend(self, *, player, base_card, card):
        self._player(player).remove_card(card=card)
        self._table.stack_card(base_card=base_card, card=card)
        self._clear_yields()

    def yield_attack(self, *, player):
        self._player(player).add_status(Status.YIELDED)
        if not self._no_more_attacks():
            return

        if self._collector:
            self.collect()
            return

        self._successful_defense_cleanup()

    def collect(self):
        self._collector.take_cards(cards=self._table.collect())
        self.draw()
        self._rotate(skip=1)
        self._collector.remove_status(Status.COLLECTING)
        self._clear_yields()
        self._compact_hands()

    def _successful_defense_cleanup(self):
        self._table.clear()
        self.draw()
        self._rotate()
        self._clear_yields()
        self._compact_hands()

    def draw(self):
        players = self._ordered_players_with_cards_in_round()
        player_count = len(players)
        for index in range(player_count):
            index_with_passes = (index - self._pass_count) % player_count
            player = players[index_with_passes]
            player.draw(draw_pile=self._draw_pile)
        self._pass_count = 0

    def _pass_card(self, *, player, card):
        self._player(player).remove_card(card=card)
        self._table.add_card(card=card)

    def pass_cards(self, *, player, cards):
        for card in cards:
            self._pass_card(player=player, card=card)
        self._pass_count += 1
        self._clear_yields()
        self._rotate()

    def give_up(self, *, player):
        self._player(player).add_status(Status.COLLECTING)
        self._clear_yields()

    def organize_cards(self, *, player, strategy):
        self._player(player).organize_cards(
            strategy=strategy, trump_suit=self._trump_suit
        )

    def _rotate(self, *, skip=0):
        players = self._ordered_players_with_cards_in_round()
        shift = skip + 1
        for index, player in enumerate(players):
            player.order = (index - shift) % len(players)

    def _compact_hands(self):
        for player in self._ordered_players_with_cards_in_round():
            player.compact_hand()

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

    def _no_more_attacks(self):
        return set(self._attackers()).issubset(set(self._yielded_players()))

    def _yielded_players(self):
        return [
            player
            for player in self._active_players()
            if player.has_status(Status.YIELDED)
        ]

    def _clear_yields(self):
        for _player in self._ordered_players():
            _player.remove_status(Status.YIELDED)

    def _active_players(self):
        return [
            player
            for player in self._ordered_players()
            if self._draw_pile.size() or player.cards()
        ]

    def _ordered_players_with_cards_in_round(self):
        return [
            player
            for player in self._ordered_players()
            if player.had_cards_in_round() or self._draw_pile.size()
        ]

    def _ordered_players(self):
        return sorted(self._players.values(), key=attrgetter("order"))
