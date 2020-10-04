# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    "test_scenarios[cannot_attack_with_unmatched_rank.json] 1"
] = '{"no_display": true, "type": "attacked_with_many", "to_state":{"durak":null,"hands":{"john":["KC","KH","QC","JS","6S","7C"],"cyril":["QH","6C","JC","6D","7D","7H","JH","7S","AS","JD","KD","AH"],"kevin":["AC","AD","KS","QD","6H","QS"],"maxim":["10H","8S","9S","8C","9C","8H","9H","8D","10D","9D","10C","10S"]},"table":[],"players":["cyril","kevin","john","maxim"],"winners":[],"yielded":[],"defender":"kevin","attackers":["cyril"],"collector":null,"draw_pile":[],"pass_count":0,"trump_suit":"clubs","lowest_rank":"6","attack_limit":6,"legal_passes":{"cards":[],"limit":6},"with_passing":true,"legal_attacks":{"cards":["QH","7D","JH","6D","JC","AS","JD","7H","7S","AH","6C","KD"],"limit":6},"legal_defenses":{}},"payload":{"cards":["KD","6D"]},"user":"cyril"}'
