import pytest

from lib.durak.draw_pile import DrawPile


@pytest.fixture
def get_all_cards_shuffled(mocker):
    return mocker.patch(
        "lib.durak.draw_pile.get_all_cards_shuffled",
        mocker.MagicMock(return_value=["10D", "10C", "2S", "5C", "8D", "2C"]),
    )


def test_draw_pile_size(get_all_cards_shuffled):
    seed = 0.4
    subject = DrawPile(drawn_cards=[], seed=seed, lowest_rank="2")
    assert subject.size() == 6
    # TODO: remove
    assert subject.serialize() == ["10D", "10C", "2S", "5C", "8D", "2C"]
    get_all_cards_shuffled.assert_called_with(seed)


def test_drawn_cards(get_all_cards_shuffled):
    seed = 0.4
    subject = DrawPile(drawn_cards=["10D", "10C"], seed=seed, lowest_rank="2")
    assert subject.size() == 4
    # TODO: remove
    assert subject.serialize() == ["2S", "5C", "8D", "2C"]
    get_all_cards_shuffled.assert_called_with(seed)


def test_lowest_rank_is_six(get_all_cards_shuffled):
    seed = 0.4
    subject = DrawPile(drawn_cards=[], seed=seed, lowest_rank="6")
    assert subject.size() == 3
    # TODO: remove
    assert subject.serialize() == ["10D", "10C", "8D"]
    get_all_cards_shuffled.assert_called_with(seed)


def test_draw_from_pile(get_all_cards_shuffled):
    seed = 0.4
    subject = DrawPile(drawn_cards=[], seed=seed, lowest_rank="2")
    assert subject.draw(count=2) == ["10D", "10C"]
    # TODO: remove
    assert subject.serialize() == ["2S", "5C", "8D", "2C"]
    get_all_cards_shuffled.assert_called_with(seed)
