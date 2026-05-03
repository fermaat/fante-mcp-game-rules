import random
import re
from typing import Protocol

from mcp_game_rules.domain.dice import DicePolicy, PlotDieFace
from mcp_game_rules.domain.results import RollResult

_DICE_RE = re.compile(
    r"^(?P<count>[1-9]\d*)?d(?P<sides>[1-9]\d*)(?P<mod>[+-][1-9]\d*)?$",
    re.IGNORECASE,
)


class _RngLike(Protocol):
    def randint(self, a: int, b: int) -> int: ...


def _plot_face(value: int) -> PlotDieFace:
    if value <= 2:
        return PlotDieFace.OPPORTUNITY
    if value <= 4:
        return PlotDieFace.COMPLICATION
    return PlotDieFace.BLANK


class SystemDice:
    """DiceRoller implementation using the standard library's RNG."""

    def __init__(self, rng: _RngLike | None = None) -> None:
        self._rng: _RngLike = rng if rng is not None else random.SystemRandom()

    def roll_spec(self, spec: str) -> RollResult:
        m = _DICE_RE.match(spec.strip())
        if not m:
            raise ValueError(f"Invalid dice spec: {spec!r}. Expected format: XdY, XdY+Z, dY, etc.")
        count = int(m.group("count") or 1)
        sides = int(m.group("sides"))
        mod = int(m.group("mod") or 0)
        if sides < 2:
            raise ValueError(f"Dice must have at least 2 sides, got {sides}")
        rolls = [self._rng.randint(1, sides) for _ in range(count)]
        breakdown = rolls + ([mod] if mod != 0 else [])
        return RollResult(spec=spec, total=sum(rolls) + mod, breakdown=breakdown)

    def execute_policy(self, policy: DicePolicy) -> tuple[list[int], int, list[PlotDieFace]]:
        """Returns (d20_rolls, kept_roll, plot_dice_faces)."""
        d20_rolls = [self._rng.randint(1, 20) for _ in range(policy.d20s)]
        if policy.keep == "highest":
            kept = max(d20_rolls)
        elif policy.keep == "lowest":
            kept = min(d20_rolls)
        else:
            kept = sum(d20_rolls)
        plot_faces = [_plot_face(self._rng.randint(1, 6)) for _ in range(policy.plot_dice)]
        return d20_rolls, kept, plot_faces
