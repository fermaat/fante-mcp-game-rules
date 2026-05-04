import pytest

from mcp_game_rules.domain.actor import Actor
from mcp_game_rules.domain.attributes import Attributes
from mcp_game_rules.engine.checker import SystemChecker
from mcp_game_rules.engine.dice import SystemDice
from mcp_game_rules.packs.loader import load_builtin_packs
from tests.conftest import FakeRng


@pytest.fixture(scope="module")
def physics_pack():
    return next(p for p in load_builtin_packs() if p.pack_name == "physics_basic")


@pytest.fixture(scope="module")
def fante():
    return Actor(
        name="Fante",
        attributes=Attributes(strength=2, speed=3),
        skills={"athletics": 1},
    )


@pytest.mark.functional
def test_basic_climb_success(physics_pack, fante):
    climb = next(r for r in physics_pack.rules if r.id == "climb")
    checker = SystemChecker(SystemDice(FakeRng([15])))
    result = checker.resolve(climb, fante, {}, physics_pack.default_dice_policy)

    assert result.success is True
    assert result.kept_roll == 15
    assert result.attribute_bonus == 2
    assert result.skill_bonus == 1
    assert result.applied_modifiers == []
    assert result.total == 18  # 15 + 2 + 1


@pytest.mark.functional
def test_wet_surface_modifier_fires(physics_pack, fante):
    climb = next(r for r in physics_pack.rules if r.id == "climb")
    checker = SystemChecker(SystemDice(FakeRng([15])))
    result = checker.resolve(climb, fante, {"surface": "wet"}, physics_pack.default_dice_policy)

    assert result.situational_modifier == 5
    assert len(result.applied_modifiers) == 1
    assert result.applied_modifiers[0].delta == 5
    assert result.success is True
    assert result.narration_seed == "You scramble up with effort."


@pytest.mark.functional
def test_low_roll_failure(physics_pack, fante):
    climb = next(r for r in physics_pack.rules if r.id == "climb")
    checker = SystemChecker(SystemDice(FakeRng([3])))
    result = checker.resolve(climb, fante, {}, physics_pack.default_dice_policy)

    assert result.success is False
    assert result.total == 6  # 3 + 2 + 1
    assert result.narration_seed == "You slip and fall back down."


@pytest.mark.functional
def test_disadvantage_keep_lowest(physics_pack, fante):
    dodge = next(r for r in physics_pack.rules if r.id == "dodge_falling_rocks")
    checker = SystemChecker(SystemDice(FakeRng([18, 4])))
    result = checker.resolve(dodge, fante, {}, physics_pack.default_dice_policy)

    assert result.d20_rolls == [18, 4]
    assert result.kept_roll == 4
