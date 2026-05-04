"""Integration tests — spawns the MCP stdio server as a subprocess and exercises
all tools and one resource via the mcp SDK client."""

import sys
from typing import Any

import pytest
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from pydantic import AnyUrl

from mcp_game_rules.domain.actor import Actor
from mcp_game_rules.domain.attributes import Attributes
from mcp_game_rules.domain.pack import RulePack

pytestmark = pytest.mark.integration

_SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", "mcp_game_rules"],
)

_ACTOR = Actor(
    name="Fante",
    attributes=Attributes(strength=3, speed=2),
    skills={"athletics": 1},
)


async def test_list_rules() -> None:
    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()
            result = await s.call_tool("list_rules", {})
    assert not result.isError
    rules: list[str] = result.structuredContent["result"]  # type: ignore[index]
    assert isinstance(rules, list)
    assert "climb" in rules


async def test_roll() -> None:
    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()
            result = await s.call_tool("roll", {"spec": "1d20"})
    assert not result.isError
    data: dict[str, Any] = result.structuredContent  # type: ignore[assignment]
    assert "total" in data
    assert isinstance(data["total"], int)


async def test_describe_rule() -> None:
    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()
            result = await s.call_tool("describe_rule", {"rule_id": "climb"})
    assert not result.isError
    text: str = result.content[0].text  # type: ignore[union-attr]
    assert "climb" in text.lower()


async def test_check_climb() -> None:
    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()
            result = await s.call_tool(
                "check",
                {
                    "rule_id": "climb",
                    "actor": _ACTOR.model_dump(),
                    "context": {"surface": "wet"},
                },
            )
    assert not result.isError
    data: dict[str, Any] = result.structuredContent  # type: ignore[assignment]
    assert data["rule_id"] == "climb"
    assert data["total"] == (
        data["kept_roll"]
        + data["attribute_bonus"]
        + data["skill_bonus"]
        + data["situational_modifier"]
    )


async def test_check_climb_with_player_score() -> None:
    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()
            result = await s.call_tool(
                "check",
                {
                    "rule_id": "climb",
                    "actor": _ACTOR.model_dump(),
                    "context": {"surface": "wet"},
                    "player_score": 14,
                },
            )
    assert not result.isError
    data: dict[str, Any] = result.structuredContent  # type: ignore[assignment]
    assert data["d20_rolls"] == []
    assert data["kept_roll"] == 14
    assert data["situational_modifier"] == 5
    # 14 (score) + 3 (str) + 1 (athletics) + 5 (wet) = 23
    assert data["total"] == 23
    assert data["success"] is True


async def test_read_resource_physics_pack() -> None:
    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()
            result = await s.read_resource(AnyUrl("rule-pack://physics_basic"))
    assert result.contents
    raw: str = result.contents[0].text  # type: ignore[union-attr]
    pack = RulePack.model_validate_json(raw)
    assert pack.pack_name == "physics_basic"
    assert any(r.id == "climb" for r in pack.rules)
