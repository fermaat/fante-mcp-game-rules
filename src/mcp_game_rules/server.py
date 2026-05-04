"""MCP stdio server — exposes the rule engine as tools and resources."""

from typing import Any

from mcp.server.fastmcp import FastMCP

from mcp_game_rules.domain.actor import Actor
from mcp_game_rules.domain.dice import DicePolicy
from mcp_game_rules.engine.composite import CompositeRuleEngine

_engine = CompositeRuleEngine.from_settings()
mcp = FastMCP("mcp-game-rules")


@mcp.tool()
def roll(spec: str) -> dict[str, Any]:
    """Roll dice using a dice spec string (e.g. '2d6+3')."""
    return _engine.roll(spec).model_dump()


@mcp.tool()
def check(
    rule_id: str,
    actor: dict[str, Any],
    context: dict[str, Any] | None = None,
    dice_override: dict[str, Any] | None = None,
    player_score: int | None = None,
) -> dict[str, Any]:
    """Resolve an action check for an actor against a rule.

    actor: Actor serialised as a dict (use Actor.model_dump()).
    context: optional situational key/value pairs (e.g. {"surface": "wet"}).
    dice_override: optional DicePolicy serialised as a dict.
    player_score: if provided, replaces the d20 roll with this value (skill mode).
        Plot dice still roll per policy. d20_rolls in the result will be empty.
    """
    actor_obj = Actor.model_validate(actor)
    policy = DicePolicy.model_validate(dice_override) if dice_override else None
    return _engine.check(rule_id, actor_obj, context or {}, policy, player_score).model_dump()


@mcp.tool()
def describe_rule(rule_id: str) -> str:
    """Return a human-readable description of a rule."""
    return _engine.describe_rule(rule_id)


@mcp.tool()
def list_rules() -> list[str]:
    """Return all rule IDs available across loaded packs."""
    return _engine.list_rules()


@mcp.resource("rule-pack://{pack_name}")
def get_rule_pack(pack_name: str) -> str:
    """Return a loaded rule pack serialised as JSON."""
    packs = _engine.loaded_packs()
    if pack_name not in packs:
        raise KeyError(f"Pack '{pack_name}' not loaded")
    return packs[pack_name].model_dump_json()


def run() -> None:
    mcp.run(transport="stdio")
