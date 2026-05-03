from mcp_game_rules.domain.attributes import Attribute
from mcp_game_rules.domain.conditions import Condition
from mcp_game_rules.domain.dice import DicePolicy
from mcp_game_rules.domain.pack import Modifier, Rule
from mcp_game_rules.engine.format import pretty_rule

_SAMPLE_RULE = Rule(
    id="climb",
    description="Attempt to climb a rocky surface.",
    attribute=Attribute.STRENGTH,
    skill="athletics",
    base_difficulty=10,
    dice_policy=None,
    modifiers=[
        Modifier(
            when=Condition(field="context.surface", op="eq", value="wet"),
            delta=-2,
            reason="wet surface",
        )
    ],
    on_success="You scramble up with effort.",
    on_failure="You slip and fall back down.",
    complexity_tier=1,
)

_EXPECTED = """\
Rule: climb
Description: Attempt to climb a rocky surface.
Attribute: strength | Skill: athletics
DC: 10 | Tier: 1
Dice policy: pack default
Modifiers:
  - context.surface eq wet → -2  (wet surface)
On success: You scramble up with effort.
On failure: You slip and fall back down."""


def test_pretty_rule_full_output():
    assert pretty_rule(_SAMPLE_RULE) == _EXPECTED


def test_pretty_rule_contains_rule_id():
    output = pretty_rule(_SAMPLE_RULE)
    assert "climb" in output


def test_pretty_rule_contains_attribute():
    output = pretty_rule(_SAMPLE_RULE)
    assert "strength" in output


def test_pretty_rule_contains_dc():
    output = pretty_rule(_SAMPLE_RULE)
    assert "DC: 10" in output


def test_pretty_rule_contains_modifier_reason():
    output = pretty_rule(_SAMPLE_RULE)
    assert "wet surface" in output


def test_pretty_rule_contains_success_and_failure_seeds():
    output = pretty_rule(_SAMPLE_RULE)
    assert "You scramble up with effort." in output
    assert "You slip and fall back down." in output


def test_pretty_rule_with_pack_default_policy():
    policy = DicePolicy(d20s=2, keep="highest", plot_dice=1)
    output = pretty_rule(_SAMPLE_RULE, pack_default_policy=policy)
    assert "2d20 keep=highest plot=1 (pack default)" in output


def test_pretty_rule_no_modifiers():
    rule = Rule(id="rest", description="Take a short rest.", base_difficulty=5)
    output = pretty_rule(rule)
    assert "Modifiers: none" in output


def test_pretty_rule_no_success_failure():
    rule = Rule(id="rest", description="Take a short rest.", base_difficulty=5)
    output = pretty_rule(rule)
    assert "On success" not in output
    assert "On failure" not in output
