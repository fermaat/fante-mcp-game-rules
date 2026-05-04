"""mcp-game-rules — MCP server exposing data-driven game rules for the Fante RPG."""

__version__ = "0.2.0"

from mcp_game_rules.domain.actor import Actor
from mcp_game_rules.domain.attributes import Attribute, Attributes
from mcp_game_rules.domain.conditions import Condition
from mcp_game_rules.domain.dice import DicePolicy, PlotDieFace
from mcp_game_rules.domain.effects import Effect
from mcp_game_rules.domain.pack import Modifier, Rule, RulePack
from mcp_game_rules.domain.results import CheckResult, RollResult
from mcp_game_rules.engine.composite import CompositeRuleEngine

__all__ = [
    "Actor",
    "Attribute",
    "Attributes",
    "CheckResult",
    "CompositeRuleEngine",
    "Condition",
    "DicePolicy",
    "Effect",
    "Modifier",
    "PlotDieFace",
    "Rule",
    "RulePack",
    "RollResult",
]
