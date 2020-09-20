# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    "test_scenarios[started_game.json] 1"
] = '{"type": "started_game", "to_state": {"durak": null, "hands": {"anna": ["10C", "QC", "JS", "6S", "9D", "7S"], "igor": ["KC", "9H", "QH", "JC", "8H", "10H"], "vasyl": ["QD", "AS", "10D", "7H", "10S", "9C"], "grusha": ["QS", "KH", "AD", "KD", "JH", "8S"]}, "table": [], "players": ["anna", "vasyl", "igor", "grusha"], "winners": [], "yielded": [], "defender": "vasyl", "attackers": ["anna"], "draw_pile": ["AH", "6C", "7C", "7D", "6D", "6H", "AC", "8D", "9S", "KS", "8C", "JD"], "pass_count": 0, "trump_suit": "diamonds", "lowest_rank": "6", "attack_limit": 100, "legal_passes": {"cards": [], "limit": 6}, "with_passing": true, "legal_attacks": {"cards": ["10C", "6S", "7S", "9D", "JS", "QC"], "limit": 6}, "legal_defenses": {}, "collector": null}, "user": "anna", "payload": {}}'

snapshots[
    "test_scenarios[passed_with_last_card.json] 1"
] = '{"type": "passed_with_many", "user": "anna", "payload": {"cards": ["10H"]}, "to_state": {"durak": null, "hands": {"anna": [null], "igor": ["9S", "QC"], "vasyl": ["AH", "10C"], "grusha": ["QS", null, "KH"]}, "table": [["10D"], ["10H"]], "players": ["anna", "vasyl", "igor", "grusha"], "winners": ["anna"], "yielded": [], "defender": "vasyl", "attackers": ["igor", "grusha"], "draw_pile": [], "pass_count": 1, "trump_suit": "hearts", "lowest_rank": "6", "attack_limit": 100, "legal_passes": {"cards": ["10C"], "limit": 0}, "with_passing": true, "legal_attacks": {"cards": [], "limit": 0}, "legal_defenses": {"10D": ["AH"], "10H": ["AH"]}, "collector": null}}'

snapshots[
    "test_scenarios[defend_successfully_after_attack_plays_last_card.json] 1"
] = '{"type": "yielded_attack", "user": "igor", "payload": {}, "to_state": {"durak": null, "hands": {"anna": ["KS", "JD"], "igor": ["9S", "QD", "6S", "6D", "JS"], "vasyl": ["JC", "QS", "8C", "QH", "6H"], "grusha": []}, "table": [], "players": ["anna", "vasyl", "igor", "grusha"], "winners": ["grusha"], "yielded": [], "defender": "vasyl", "attackers": ["anna"], "draw_pile": [], "pass_count": 0, "trump_suit": "spades", "lowest_rank": "6", "attack_limit": 100, "legal_passes": {"cards": [], "limit": 5}, "with_passing": true, "legal_attacks": {"cards": ["JD", "KS"], "limit": 5}, "legal_defenses": {}, "collector": null}}'

snapshots[
    "test_scenarios[collect_rotates_properly.json] 1"
] = '{"type": "yielded_attack", "user": "anna", "payload": {}, "to_state": {"durak": null, "hands": {"anna": [], "igor": ["9S", "6S", "6D", "JD", "QD", "JC", "JS", "QH", "QS"], "vasyl": ["8C", "6H", "KS"], "grusha": []}, "table": [], "players": ["igor", "anna", "vasyl", "grusha"], "winners": ["anna", "grusha"], "yielded": [], "defender": "vasyl", "attackers": ["igor"], "draw_pile": [], "pass_count": 0, "trump_suit": "spades", "lowest_rank": "6", "attack_limit": 100, "legal_passes": {"cards": [], "limit": 9}, "with_passing": true, "legal_attacks": {"cards": ["6D", "6S", "9S", "JC", "JD", "JS", "QD", "QH", "QS"], "limit": 3}, "legal_defenses": {}, "collector": null}}'

snapshots[
    "test_scenarios[yielding_when_defender_wins.json] 1"
] = '{"type": "yielded_attack", "user": "grusha", "payload": {}, "to_state": {"hands": {"anna": [], "igor": ["KC", "6D"], "vasyl": ["AC", "8H", "10D", "AS", "9C", "9H", "QD", "9S"], "grusha": ["KH", "AD", "KD", "JH"]}, "table": [], "players": ["anna", "vasyl", "igor", "grusha"], "winners": ["anna"], "yielded": [], "defender": "igor", "attackers": ["vasyl"], "draw_pile": [], "pass_count": 0, "trump_suit": "diamonds", "lowest_rank": "6", "attack_limit": 100, "legal_passes": {"cards": [], "limit": 4}, "with_passing": true, "legal_attacks": {"cards": ["10D", "8H", "9C", "9H", "9S", "AC", "AS", "QD"], "limit": 2}, "legal_defenses": {}, "durak": null, "collector": null}}'
