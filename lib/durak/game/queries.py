from itertools import chain


class Base:
    @classmethod
    def result(cls, *, game):
        return cls(game=game)._result

    def __init__(self, *, game):
        self._game = game

    @property
    def _result(self):
        raise NotImplementedError

    @property
    def _defender(self):
        return self._game._defender()


class LegalAttacks(Base):
    @property
    def _result(self):
        return {
            "cards": self._cards,
            "limit": self._limit,
        }

    @property
    def _cards(self):
        if self._defender is None:
            return set()

        attackers = self._game._attackers()
        attacker_cards = chain.from_iterable(player.cards() for player in attackers)
        return set(attacker_cards) & self._game._table.legal_attacks()

    @property
    def _limit(self):
        if self._defender is None:
            return 0

        attack_limit = min(len(self._defender.cards()), self._game._attack_limit)
        undefended_cards = len(self._game._table.undefended_cards())
        return max(0, attack_limit - undefended_cards)


class LegalDefenses(Base):
    @property
    def _result(self):
        if self._game._collector:
            return {}

        if self._defender is None:
            return {}

        defender_cards = set(self._defender.cards())
        return {
            base_card: defender_cards & cards
            for base_card, cards in self._legal_defenses_for_table_cards.items()
        }

    @property
    def _legal_defenses_for_table_cards(self):
        return self._game._table.legal_defenses(trump_suit=self._game._trump_suit)


class LegalPasses(Base):
    @property
    def _result(self):
        if self._pass_recipient is None:
            return {"cards": set(), "limit": 0}

        return {
            "cards": self._cards,
            "limit": self._limit,
        }

    @property
    def _cards(self):
        if self._pass_recipient is None:
            return set()

        return set(self._defender.cards()) & self._game._table.legal_passes()

    @property
    def _limit(self):
        if self._pass_recipient is None:
            return 0

        recipient_card_count = len(self._pass_recipient.cards())
        attack_limit = min(recipient_card_count, self._game._attack_limit)
        undefended_card_count = len(self._game._table.undefended_cards())

        return max(0, attack_limit - undefended_card_count)

    @property
    def _pass_recipient(self):
        if not self._defender:
            return

        players = self._game._ordered_players_with_cards_in_round()
        players_from_defender = players[2:] + [players[0]]
        next_players_with_cards = [
            player for player in players_from_defender if player.cards()
        ]
        if not next_players_with_cards:
            return
        return next_players_with_cards[0]
