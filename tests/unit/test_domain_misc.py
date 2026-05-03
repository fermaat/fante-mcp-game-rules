from mcp_game_rules.domain.actor import Actor
from mcp_game_rules.domain.attributes import Attribute, Attributes
from mcp_game_rules.domain.effects import Effect
from mcp_game_rules.domain.results import RollResult


def test_actor_defaults():
    actor = Actor(name="Fante")
    assert actor.name == "Fante"
    assert actor.attributes == Attributes()
    assert actor.skills == {}
    assert actor.tags == []


def test_actor_with_all_fields():
    actor = Actor(
        name="Fante",
        attributes=Attributes(strength=3, speed=2),
        skills={"athletics": 1, "acrobatics": 2},
        tags=["wet", "tired"],
    )
    assert actor.attributes.get(Attribute.STRENGTH) == 3
    assert actor.skills["athletics"] == 1
    assert "wet" in actor.tags


def test_effect_defaults():
    effect = Effect(name="wet")
    assert effect.magnitude == 1
    assert effect.duration_turns is None
    assert effect.source_rule_id is None


def test_effect_with_duration():
    effect = Effect(name="blessed", magnitude=2, duration_turns=3, source_rule_id="spark_of_light")
    assert effect.duration_turns == 3
    assert effect.source_rule_id == "spark_of_light"


def test_roll_result_str():
    result = RollResult(spec="2d6+3", total=9, breakdown=[4, 2, 3])
    assert str(result) == "2d6+3 → [4 + 2 + 3] = 9"


def test_roll_result_str_no_modifier():
    result = RollResult(spec="d20", total=15, breakdown=[15])
    assert str(result) == "d20 → [15] = 15"
