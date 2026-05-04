from mcp_game_rules.domain.actor import Actor
from mcp_game_rules.domain.dice import DicePolicy
from mcp_game_rules.domain.pack import Rule, RulePack
from mcp_game_rules.domain.results import CheckResult, RollResult
from mcp_game_rules.engine.format import pretty_rule
from mcp_game_rules.protocols import CheckResolver, DiceRoller


class CompositeRuleEngine:
    def __init__(
        self,
        packs: list[RulePack],
        dice: DiceRoller,
        checker: CheckResolver,
    ) -> None:
        self._dice = dice
        self._checker = checker
        self._index: dict[str, tuple[RulePack, Rule]] = {}
        for pack in packs:
            for rule in pack.rules:
                if rule.id in self._index:
                    existing = self._index[rule.id][0]
                    raise ValueError(
                        f"Rule id conflict: '{rule.id}' found in both "
                        f"'{existing.pack_name}' and '{pack.pack_name}'"
                    )
                self._index[rule.id] = (pack, rule)

    def roll(self, spec: str) -> RollResult:
        return self._dice.roll_spec(spec)

    def check(
        self,
        rule_id: str,
        actor: Actor,
        context: dict[str, object],
        dice_override: DicePolicy | None = None,
    ) -> CheckResult:
        if rule_id not in self._index:
            raise KeyError(f"Rule '{rule_id}' not found in loaded packs")
        pack, rule = self._index[rule_id]
        result = self._checker.resolve(
            rule, actor, context, pack.default_dice_policy, dice_override
        )
        return result.model_copy(update={"pack_name": pack.pack_name})

    def describe_rule(self, rule_id: str) -> str:
        if rule_id not in self._index:
            raise KeyError(f"Rule '{rule_id}' not found in loaded packs")
        pack, rule = self._index[rule_id]
        return pretty_rule(rule, pack.default_dice_policy)

    def list_rules(self) -> list[str]:
        return sorted(self._index.keys())
