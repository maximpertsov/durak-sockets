import pytest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)


@pytest.fixture
def get_draw_pile_cards(mocker):
    def wrapped(cards):
        return mocker.patch(
            "lib.durak.draw_pile.get_all_cards_shuffled",
            mocker.MagicMock(return_value=cards),
        )

    return wrapped
