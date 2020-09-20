import glob
import json
import os

import pytest

from main import handle_durak_message

SCENARIO_INPUT_FILES = glob.glob(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "scenario_inputs", "*.json"
    )
)


@pytest.fixture
def assert_handle_message(mocker):
    mocked_persist = mocker.patch("main.persist")

    async def wrapped(from_state, to_state):
        result = await handle_durak_message(from_state)
        assert json.loads(result) == json.loads(to_state)
        mocked_persist.assert_called_once()

    return wrapped


@pytest.fixture
def assert_snapshot_matches(assert_handle_message, snapshot):
    async def wrapped(input_path):
        with open(input_path, "r") as f:
            actual = await handle_durak_message(f.read())
            snapshot.assert_match(actual)

    return wrapped


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_path", SCENARIO_INPUT_FILES, ids=lambda p: os.path.split(p)[1]
)
async def test_scenarios(input_path, assert_snapshot_matches):
    await assert_snapshot_matches(input_path)
