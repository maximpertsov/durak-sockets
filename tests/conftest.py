import json
import os
import sys

from snapshottest.formatters import BaseFormatter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)


def _assert_value_matches_snapshot(self, test, test_value, snapshot_value, formatter):
    test.assert_equals(
        json.loads(formatter.normalize(test_value)), json.loads(snapshot_value)
    )


BaseFormatter.assert_value_matches_snapshot = _assert_value_matches_snapshot
