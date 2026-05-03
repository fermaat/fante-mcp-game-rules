import pytest

from mcp_game_rules.domain.dice import DicePolicy, PlotDieFace
from mcp_game_rules.engine.dice import SystemDice
from tests.conftest import FakeRng


def test_roll_spec_two_d6_plus_modifier():
    dice = SystemDice(rng=FakeRng([4, 2]))
    result = dice.roll_spec("2d6+3")
    assert result.total == 9
    assert result.breakdown == [4, 2, 3]
    assert result.spec == "2d6+3"


def test_roll_spec_implicit_count():
    dice = SystemDice(rng=FakeRng([15]))
    result = dice.roll_spec("d20")
    assert result.total == 15
    assert result.breakdown == [15]


def test_roll_spec_no_modifier_omits_zero_from_breakdown():
    dice = SystemDice(rng=FakeRng([6, 3]))
    result = dice.roll_spec("2d6")
    assert result.breakdown == [6, 3]
    assert result.total == 9


def test_roll_spec_negative_modifier():
    dice = SystemDice(rng=FakeRng([10]))
    result = dice.roll_spec("d20-3")
    assert result.total == 7
    assert result.breakdown == [10, -3]


def test_roll_spec_invalid_raises():
    dice = SystemDice(rng=FakeRng([]))
    with pytest.raises(ValueError):
        dice.roll_spec("garbage")


def test_roll_spec_empty_raises():
    dice = SystemDice(rng=FakeRng([]))
    with pytest.raises(ValueError):
        dice.roll_spec("")


def test_execute_policy_keep_highest():
    dice = SystemDice(rng=FakeRng([14, 7, 1]))
    policy = DicePolicy(d20s=2, keep="highest", plot_dice=1)
    d20_rolls, kept, plot = dice.execute_policy(policy)
    assert d20_rolls == [14, 7]
    assert kept == 14
    assert plot == [PlotDieFace.OPPORTUNITY]


def test_execute_policy_keep_lowest():
    dice = SystemDice(rng=FakeRng([14, 7, 1]))
    policy = DicePolicy(d20s=2, keep="lowest", plot_dice=1)
    d20_rolls, kept, plot = dice.execute_policy(policy)
    assert d20_rolls == [14, 7]
    assert kept == 7
    assert plot == [PlotDieFace.OPPORTUNITY]


@pytest.mark.parametrize(
    "face_value,expected",
    [
        (1, PlotDieFace.OPPORTUNITY),
        (2, PlotDieFace.OPPORTUNITY),
        (3, PlotDieFace.COMPLICATION),
        (4, PlotDieFace.COMPLICATION),
        (5, PlotDieFace.BLANK),
        (6, PlotDieFace.BLANK),
    ],
)
def test_plot_die_face_mapping(face_value: int, expected: PlotDieFace):
    dice = SystemDice(rng=FakeRng([10, face_value]))
    policy = DicePolicy(d20s=1, keep="highest", plot_dice=1)
    _, _, plot = dice.execute_policy(policy)
    assert plot[0] == expected


def test_execute_policy_no_plot_dice():
    dice = SystemDice(rng=FakeRng([12]))
    policy = DicePolicy(d20s=1, keep="highest", plot_dice=0)
    d20_rolls, kept, plot = dice.execute_policy(policy)
    assert d20_rolls == [12]
    assert kept == 12
    assert plot == []
