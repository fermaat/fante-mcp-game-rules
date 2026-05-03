from typing import Literal, Self

from pydantic import BaseModel, Field, model_validator

from mcp_game_rules.domain.attributes import Attribute
from mcp_game_rules.domain.conditions import Condition
from mcp_game_rules.domain.dice import DicePolicy


class Modifier(BaseModel):
    when: Condition
    delta: int
    reason: str


class Rule(BaseModel):
    id: str
    description: str
    attribute: Attribute | None = None
    skill: str | None = None
    base_difficulty: int
    dice_policy: DicePolicy | None = None
    modifiers: list[Modifier] = Field(default_factory=list)
    on_success: str | None = None
    on_failure: str | None = None
    complexity_tier: int = Field(1, ge=1, le=5)


class RulePack(BaseModel):
    schema_version: int = 1
    pack_name: str
    pack_version: str
    domain: Literal["physical", "magical", "environmental", "social"]
    complexity_tier: int = Field(1, ge=1, le=5)
    description: str
    default_dice_policy: DicePolicy = Field(default_factory=DicePolicy)
    skills: dict[str, Attribute] = Field(default_factory=dict)
    rules: list[Rule]

    @model_validator(mode="after")
    def _check_unique_rule_ids(self) -> Self:
        seen: set[str] = set()
        for rule in self.rules:
            if rule.id in seen:
                raise ValueError(f"Duplicate rule id in pack '{self.pack_name}': '{rule.id}'")
            seen.add(rule.id)
        return self
