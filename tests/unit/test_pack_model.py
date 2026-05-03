from typing import Any

import pytest
from pydantic import ValidationError

from mcp_game_rules.domain.pack import Rule, RulePack


def _minimal_pack(**overrides: Any) -> RulePack:
    defaults = dict(
        pack_name="test_pack",
        pack_version="1.0.0",
        domain="physical",
        description="A minimal test pack.",
        rules=[Rule(id="climb", description="Climb something.", base_difficulty=10)],
    )
    defaults.update(overrides)
    return RulePack(**defaults)


def test_duplicate_rule_ids_raises():
    with pytest.raises(ValidationError, match="Duplicate rule id"):
        RulePack(
            pack_name="test_pack",
            pack_version="1.0.0",
            domain="physical",
            description="test",
            rules=[
                Rule(id="climb", description="first", base_difficulty=10),
                Rule(id="climb", description="second", base_difficulty=12),
            ],
        )


def test_unique_rule_ids_valid():
    pack = _minimal_pack(
        rules=[
            Rule(id="climb", description="first", base_difficulty=10),
            Rule(id="swim", description="second", base_difficulty=12),
        ]
    )
    assert len(pack.rules) == 2


def test_round_trip_identity():
    pack = _minimal_pack()
    restored = RulePack.model_validate(pack.model_dump())
    assert restored == pack


def test_default_dice_policy_is_single_d20():
    pack = _minimal_pack()
    assert pack.default_dice_policy.d20s == 1
    assert pack.default_dice_policy.plot_dice == 0


def test_invalid_domain_raises():
    with pytest.raises(ValidationError):
        _minimal_pack(domain="underwater")


def test_complexity_tier_out_of_range_raises():
    with pytest.raises(ValidationError):
        _minimal_pack(complexity_tier=6)


def test_schema_version_defaults_to_one():
    pack = _minimal_pack()
    assert pack.schema_version == 1
