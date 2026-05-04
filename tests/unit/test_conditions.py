import pytest

from mcp_game_rules.domain.conditions import Condition
from mcp_game_rules.engine.conditions import evaluate

_SCOPE: dict[str, object] = {
    "actor": {
        "attributes": {"strength": 3, "speed": 2},
        "skills": {"athletics": 2},
        "tags": ["wet", "blessed"],
    },
    "context": {"surface": "wet", "season": "summer", "count": 5},
}


# --- eq ---


def test_eq_true():
    assert evaluate(Condition(field="context.surface", op="eq", value="wet"), _SCOPE) is True


def test_eq_false():
    assert evaluate(Condition(field="context.surface", op="eq", value="dry"), _SCOPE) is False


def test_eq_missing_field():
    assert evaluate(Condition(field="context.nonexistent", op="eq", value="x"), _SCOPE) is False


# --- neq ---


def test_neq_true():
    assert evaluate(Condition(field="context.surface", op="neq", value="dry"), _SCOPE) is True


def test_neq_false():
    assert evaluate(Condition(field="context.surface", op="neq", value="wet"), _SCOPE) is False


def test_neq_missing_field():
    assert evaluate(Condition(field="actor.missing", op="neq", value="x"), _SCOPE) is False


# --- gt / gte / lt / lte ---


def test_gt_true():
    assert evaluate(Condition(field="context.count", op="gt", value=3), _SCOPE) is True


def test_gt_false():
    assert evaluate(Condition(field="context.count", op="gt", value=5), _SCOPE) is False


def test_gte_equal():
    assert evaluate(Condition(field="context.count", op="gte", value=5), _SCOPE) is True


def test_lt_true():
    assert evaluate(Condition(field="context.count", op="lt", value=10), _SCOPE) is True


def test_lte_equal():
    assert evaluate(Condition(field="context.count", op="lte", value=5), _SCOPE) is True


def test_numeric_type_incompatible_returns_false():
    assert evaluate(Condition(field="context.surface", op="gt", value=3), _SCOPE) is False


def test_numeric_missing_field():
    assert evaluate(Condition(field="context.missing", op="gt", value=3), _SCOPE) is False


# --- in / not_in ---


def test_in_true():
    assert (
        evaluate(Condition(field="context.season", op="in", value=["summer", "autumn"]), _SCOPE)
        is True
    )


def test_in_false():
    assert (
        evaluate(Condition(field="context.season", op="in", value=["winter", "spring"]), _SCOPE)
        is False
    )


def test_in_missing_field():
    assert evaluate(Condition(field="context.missing", op="in", value=["a"]), _SCOPE) is False


def test_not_in_true():
    assert (
        evaluate(Condition(field="context.season", op="not_in", value=["winter"]), _SCOPE) is True
    )


def test_not_in_false():
    assert (
        evaluate(Condition(field="context.season", op="not_in", value=["summer"]), _SCOPE) is False
    )


# --- contains ---


def test_contains_list_true():
    assert evaluate(Condition(field="actor.tags", op="contains", value="wet"), _SCOPE) is True


def test_contains_list_false():
    assert evaluate(Condition(field="actor.tags", op="contains", value="cursed"), _SCOPE) is False


def test_contains_str_true():
    assert evaluate(Condition(field="context.surface", op="contains", value="we"), _SCOPE) is True


def test_contains_str_false():
    assert evaluate(Condition(field="context.surface", op="contains", value="dry"), _SCOPE) is False


def test_contains_missing_field():
    assert evaluate(Condition(field="actor.missing", op="contains", value="x"), _SCOPE) is False


# --- deep path resolution ---


def test_deep_nested_path():
    assert evaluate(Condition(field="actor.attributes.strength", op="gte", value=3), _SCOPE) is True


def test_partial_path_missing():
    assert evaluate(Condition(field="actor.nonexistent.depth", op="eq", value="x"), _SCOPE) is False


# --- non-dict intermediate ---


def test_non_dict_intermediate_returns_false():
    assert evaluate(Condition(field="context.count.nested", op="eq", value=1), _SCOPE) is False
