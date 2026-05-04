from typing import Protocol

from mcp_game_rules.domain.actor import Actor
from mcp_game_rules.domain.dice import DicePolicy, PlotDieFace
from mcp_game_rules.domain.pack import Rule
from mcp_game_rules.domain.results import CheckResult, RollResult


class DiceRoller(Protocol):
    def roll_spec(self, spec: str) -> RollResult: ...

    def execute_policy(self, policy: DicePolicy) -> tuple[list[int], int, list[PlotDieFace]]:
        """Returns (d20_rolls, kept_roll, plot_dice_faces)."""
        ...

    def roll_plot_dice(self, count: int) -> list[PlotDieFace]:
        """Roll only plot dice — used when the d20 is replaced by a player_score."""
        ...


class CheckResolver(Protocol):
    def resolve(
        self,
        rule: Rule,
        actor: Actor,
        context: dict[str, object],
        pack_default_policy: DicePolicy,
        dice_override: DicePolicy | None = None,
        player_score: int | None = None,
    ) -> CheckResult: ...


class RuleEngine(Protocol):
    def roll(self, spec: str) -> RollResult: ...

    def check(
        self,
        rule_id: str,
        actor: Actor,
        context: dict[str, object],
        dice_override: DicePolicy | None = None,
        player_score: int | None = None,
    ) -> CheckResult: ...

    def describe_rule(self, rule_id: str) -> str: ...

    def list_rules(self) -> list[str]: ...
