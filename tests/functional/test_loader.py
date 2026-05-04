import pytest

from mcp_game_rules.packs.loader import load_builtin_packs, load_pack


@pytest.mark.functional
def test_load_builtin_packs_returns_three():
    packs = load_builtin_packs()
    assert len(packs) == 3


@pytest.mark.functional
def test_each_builtin_pack_has_at_least_three_rules():
    packs = load_builtin_packs()
    for pack in packs:
        assert len(pack.rules) >= 3, f"{pack.pack_name!r} has fewer than 3 rules"


@pytest.mark.functional
def test_builtin_pack_names():
    names = {p.pack_name for p in load_builtin_packs()}
    assert names == {"physics_basic", "magic_basic", "environment_forest"}


@pytest.mark.functional
def test_load_malformed_yaml_raises(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("pack_name: x\nnot_valid: [}")
    with pytest.raises(ValueError):
        load_pack(bad)


@pytest.mark.functional
def test_load_missing_required_field_raises(tmp_path):
    bad = tmp_path / "missing.yaml"
    bad.write_text("pack_name: test\n")
    with pytest.raises(ValueError):
        load_pack(bad)
