from mcp_game_rules.domain.dice import DicePolicy
from mcp_game_rules.domain.pack import Rule


def pretty_rule(rule: Rule, pack_default_policy: DicePolicy | None = None) -> str:
    """Return a human-readable multi-line description of a rule."""
    lines: list[str] = []
    lines.append(f"Rule: {rule.id}")
    lines.append(f"Description: {rule.description}")

    attr_part = f"Attribute: {rule.attribute}" if rule.attribute else "Attribute: —"
    skill_part = f"Skill: {rule.skill}" if rule.skill else "Skill: —"
    lines.append(f"{attr_part} | {skill_part}")

    lines.append(f"DC: {rule.base_difficulty} | Tier: {rule.complexity_tier}")

    if rule.dice_policy is not None:
        p = rule.dice_policy
        lines.append(f"Dice policy: {p.d20s}d20 keep={p.keep} plot={p.plot_dice}")
    elif pack_default_policy is not None:
        p = pack_default_policy
        lines.append(f"Dice policy: {p.d20s}d20 keep={p.keep} plot={p.plot_dice} (pack default)")
    else:
        lines.append("Dice policy: pack default")

    if rule.modifiers:
        lines.append("Modifiers:")
        for mod in rule.modifiers:
            c = mod.when
            lines.append(f"  - {c.field} {c.op} {c.value} → {mod.delta:+d}  ({mod.reason})")
    else:
        lines.append("Modifiers: none")

    if rule.on_success:
        lines.append(f"On success: {rule.on_success}")
    if rule.on_failure:
        lines.append(f"On failure: {rule.on_failure}")

    return "\n".join(lines)
