import pytest
from pydantic import ValidationError

from mcp_game_rules.domain.attributes import Attribute, Attributes


def test_default_attributes_are_zero():
    attrs = Attributes()
    for attr in Attribute:
        assert attrs.get(attr) == 0


def test_get_returns_correct_value():
    attrs = Attributes(strength=3, speed=5)
    assert attrs.get(Attribute.STRENGTH) == 3
    assert attrs.get(Attribute.SPEED) == 5
    assert attrs.get(Attribute.INTELLECT) == 0


def test_upper_bound_valid():
    attrs = Attributes(strength=8)
    assert attrs.strength == 8


def test_strength_above_max_raises():
    with pytest.raises(ValidationError):
        Attributes(strength=9)


def test_speed_below_min_raises():
    with pytest.raises(ValidationError):
        Attributes(speed=-1)


def test_all_attributes_at_max():
    attrs = Attributes(strength=8, speed=8, intellect=8, willpower=8, awareness=8, presence=8)
    for attr in Attribute:
        assert attrs.get(attr) == 8
