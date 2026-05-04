from mcp_game_rules.domain.actor import Actor
from mcp_game_rules.domain.dice import DicePolicy
from mcp_game_rules.domain.pack import Rule
from mcp_game_rules.domain.results import AppliedModifier, CheckResult
from mcp_game_rules.engine.conditions import evaluate
from mcp_game_rules.protocols import DiceRoller


class SystemChecker:
    def __init__(self, dice: DiceRoller) -> None:
        self._dice = dice

    def resolve(
        self,
        rule: Rule,
        actor: Actor,
        context: dict[str, object],
        pack_default_policy: DicePolicy,
        dice_override: DicePolicy | None = None,
    ) -> CheckResult:
        policy = dice_override or rule.dice_policy or pack_default_policy
        scope: dict[str, object] = {"actor": actor.model_dump(), "context": context}

        d20_rolls, kept_roll, plot_faces = self._dice.execute_policy(policy)

        attribute_bonus = actor.attributes.get(rule.attribute) if rule.attribute else 0
        skill_bonus = actor.skills.get(rule.skill, 0) if rule.skill else 0

        applied: list[AppliedModifier] = []
        for mod in rule.modifiers:
            if evaluate(mod.when, scope):
                applied.append(AppliedModifier(reason=mod.reason, delta=mod.delta))

        situational = sum(m.delta for m in applied)
        total = kept_roll + attribute_bonus + skill_bonus + situational
        success = total >= rule.base_difficulty

        return CheckResult(
            rule_id=rule.id,
            pack_name="",
            d20_rolls=d20_rolls,
            kept_roll=kept_roll,
            attribute_bonus=attribute_bonus,
            skill_bonus=skill_bonus,
            situational_modifier=situational,
            total=total,
            difficulty=rule.base_difficulty,
            success=success,
            plot_dice=plot_faces,
            applied_modifiers=applied,
            narration_seed=rule.on_success if success else rule.on_failure,
        )
