# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_scenarios[started_game.json] 1'] = '{"type": "started_game", "to_state": {"durak": null, "hands": {"anna": ["10C", "QC", "JS", "6S", "9D", "7S"], "igor": ["KC", "9H", "QH", "JC", "8H", "10H"], "vasyl": ["QD", "AS", "10D", "7H", "10S", "9C"], "grusha": ["QS", "KH", "AD", "KD", "JH", "8S"]}, "table": [], "players": ["anna", "vasyl", "igor", "grusha"], "winners": [], "yielded": [], "defender": "vasyl", "attackers": ["anna"], "draw_pile": ["AH", "6C", "7C", "7D", "6D", "6H", "AC", "8D", "9S", "KS", "8C", "JD"], "pass_count": 0, "trump_suit": "diamonds", "lowest_rank": "6", "attack_limit": 100, "legal_passes": {"cards": [], "limit": 6}, "with_passing": true, "legal_attacks": {"cards": ["10C", "6S", "7S", "9D", "JS", "QC"], "limit": 6}, "legal_defenses": {}, "collector": null}, "user": "anna", "payload": {}}'
