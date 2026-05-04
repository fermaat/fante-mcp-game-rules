import pytest

from mcp_game_rules.domain.dice import DicePolicy
from mcp_game_rules.domain.pack import Rule, RulePack
from mcp_game_rules.engine.checker import SystemChecker
from mcp_game_rules.engine.composite import CompositeRuleEngine
from mcp_game_rules.engine.dice import SystemDice
from mcp_game_rules.engine.format import pretty_rule
from mcp_game_rules.packs.loader import load_builtin_packs


def _make_engine() -> CompositeRuleEngine:
    packs = load_builtin_packs()
    dice = SystemDice()
    checker = SystemChecker(dice)
    return CompositeRuleEngine(packs, dice, checker)


@pytest.mark.functional
def test_builtin_packs_no_conflict():
    engine = _make_engine()
    assert len(engine.list_rules()) > 0


@pytest.mark.functional
def test_conflict_raises_with_both_pack_names():
    packs = load_builtin_packs()
    physics = next(p for p in packs if p.pack_name == "physics_basic")
    duplicate_rule = Rule(id="climb", description="duplicate", base_difficulty=5)
    conflict_pack = RulePack(
        pack_name="conflict_pack",
        pack_version="0.1.0",
        domain="physical",
        description="pack that conflicts with physics_basic",
        rules=[duplicate_rule],
    )
    dice = SystemDice()
    checker = SystemChecker(dice)
    with pytest.raises(ValueError, match="physics_basic"):
        CompositeRuleEngine([physics, conflict_pack], dice, checker)


@pytest.mark.functional
def test_list_rules_returns_union_of_all_packs():
    engine = _make_engine()
    rules = engine.list_rules()
    assert "climb" in rules
    assert "spark_of_light" in rules
    assert "find_path" in rules
    assert rules == sorted(rules)


@pytest.mark.functional
def test_describe_rule_returns_pretty_rule_output():
    engine = _make_engine()
    output = engine.describe_rule("climb")
    packs = load_builtin_packs()
    physics = next(p for p in packs if p.pack_name == "physics_basic")
    climb = next(r for r in physics.rules if r.id == "climb")
    expected = pretty_rule(climb, physics.default_dice_policy)
    assert output == expected


@pytest.mark.functional
def test_describe_rule_unknown_raises():
    engine = _make_engine()
    with pytest.raises(KeyError):
        engine.describe_rule("nonexistent_rule")


@pytest.mark.functional
def test_pack_name_set_on_check_result():
    from mcp_game_rules.domain.actor import Actor
    from tests.conftest import FakeRng

    dice = SystemDice(FakeRng([15]))
    checker = SystemChecker(dice)
    engine = CompositeRuleEngine(load_builtin_packs(), dice, checker)
    actor = Actor(name="Test")
    result = engine.check("climb", actor, {})
    assert result.pack_name == "physics_basic"


@pytest.mark.functional
def test_engine_check_passes_player_score_through():
    from mcp_game_rules.domain.actor import Actor
    from tests.conftest import FakeRng

    dice = SystemDice(FakeRng([]))  # no d20 should be drawn
    checker = SystemChecker(dice)
    engine = CompositeRuleEngine(load_builtin_packs(), dice, checker)
    actor = Actor(name="Fante")
    result = engine.check("climb", actor, {}, player_score=18)

    assert result.pack_name == "physics_basic"
    assert result.d20_rolls == []
    assert result.kept_roll == 18
