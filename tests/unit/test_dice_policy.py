import pytest
from pydantic import ValidationError

from mcp_game_rules.domain.dice import DicePolicy


def test_defaults():
    policy = DicePolicy()
    assert policy.d20s == 1
    assert policy.keep == "highest"
    assert policy.plot_dice == 0


def test_is_advantage_true():
    policy = DicePolicy(d20s=2, keep="highest")
    assert policy.is_advantage is True
    assert policy.is_disadvantage is False


def test_is_disadvantage_true():
    policy = DicePolicy(d20s=2, keep="lowest")
    assert policy.is_disadvantage is True
    assert policy.is_advantage is False


def test_single_die_not_advantage_or_disadvantage():
    policy = DicePolicy(d20s=1, keep="highest")
    assert policy.is_advantage is False
    assert policy.is_disadvantage is False


def test_keep_all_not_advantage_or_disadvantage():
    policy = DicePolicy(d20s=2, keep="all")
    assert policy.is_advantage is False
    assert policy.is_disadvantage is False


def test_d20s_above_cap_raises():
    with pytest.raises(ValidationError):
        DicePolicy(d20s=11)


def test_d20s_zero_raises():
    with pytest.raises(ValidationError):
        DicePolicy(d20s=0)


def test_plot_dice_above_cap_raises():
    with pytest.raises(ValidationError):
        DicePolicy(plot_dice=11)


def test_plot_dice_below_zero_raises():
    with pytest.raises(ValidationError):
        DicePolicy(plot_dice=-1)
