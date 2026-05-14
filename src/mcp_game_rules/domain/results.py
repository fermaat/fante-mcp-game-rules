from pydantic import BaseModel

from mcp_game_rules.domain.dice import PlotDieFace
from mcp_game_rules.domain.pack import ChallengeCategory, ChallengeKind


class RollResult(BaseModel):
    spec: str
    total: int
    breakdown: list[int]

    def __str__(self) -> str:
        parts = " + ".join(str(x) for x in self.breakdown)
        return f"{self.spec} → [{parts}] = {self.total}"


class AppliedModifier(BaseModel):
    reason: str
    delta: int


class CheckResult(BaseModel):
    rule_id: str
    pack_name: str
    d20_rolls: list[int]
    kept_roll: int
    attribute_bonus: int
    skill_bonus: int
    situational_modifier: int
    total: int
    difficulty: int
    success: bool
    plot_dice: list[PlotDieFace]
    applied_modifiers: list[AppliedModifier]
    narration_seed: str | None
    knowledge_topic: str | None = None
    challenge: ChallengeKind = "none"
    challenge_category: ChallengeCategory | None = None
