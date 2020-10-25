import glob
import json
import os

import pytest

from lib.durak import handle_message

SCENARIO_INPUT_FILES = glob.glob(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "scenario_inputs/**/**/input.json"
    )
)
SCENARIO_OUTPUT_FILENAME = "output.json"


def format_json(json_text):
    loaded = json.loads(json_text)
    dumped = json.dumps(loaded, indent=2, sort_keys=True)

    # Add a newline
    # https://codeyarns.github.io/tech/2017-02-22-python-json-dump-misses-last-newline.html
    return dumped + "\n"


@pytest.fixture
def assert_snapshot_matches(mocker, snapshot):
    mocker.patch("lib.durak.persist")

    async def wrapped(input_path):
        with open(input_path, "r") as f:
            actual = format_json(await handle_message(f.read()))

        snapshot.snapshot_dir = os.path.dirname(input_path)
        snapshot.assert_match(actual, SCENARIO_OUTPUT_FILENAME)

    return wrapped


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_path",
    SCENARIO_INPUT_FILES,
    ids=lambda p: os.path.split(os.path.dirname(p))[1],
)
async def test_scenarios(input_path, assert_snapshot_matches):
    await assert_snapshot_matches(input_path)
