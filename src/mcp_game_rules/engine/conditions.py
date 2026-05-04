from typing import Any, Final

from mcp_game_rules.domain.conditions import Condition

_MISSING: Final = object()


def _resolve_path(scope: dict[str, object], path: str) -> object:
    keys = path.split(".")
    current: object = scope
    for key in keys:
        if not isinstance(current, dict):
            return _MISSING
        if key not in current:
            return _MISSING
        current = current[key]
    return current


def evaluate(condition: Condition, scope: dict[str, object]) -> bool:
    actual = _resolve_path(scope, condition.field)
    if actual is _MISSING:
        return False

    op = condition.op
    value: Any = condition.value

    if op == "eq":
        return bool(actual == value)
    if op == "neq":
        return bool(actual != value)
    if op in ("gt", "gte", "lt", "lte"):
        if not isinstance(actual, (int, float)) or not isinstance(value, (int, float)):
            return False
        if op == "gt":
            return actual > value
        if op == "gte":
            return actual >= value
        if op == "lt":
            return actual < value
        return actual <= value
    if op == "in":
        if not isinstance(value, list):
            return False
        return actual in value
    if op == "not_in":
        if not isinstance(value, list):
            return False
        return actual not in value
    if op == "contains":
        if isinstance(actual, (str, list)):
            return value in actual
        return False
    return False
