import importlib.resources as _pkg_res
from pathlib import Path

from core_utils import load_yaml_as, load_yaml_dir_as

from mcp_game_rules.domain.pack import RulePack


def _builtin_dir() -> Path:
    ref = _pkg_res.files("mcp_game_rules.packs").joinpath("builtin")
    return Path(str(ref))


def load_pack(path: Path) -> RulePack:
    return load_yaml_as(path, RulePack)


def load_packs(dir: Path) -> list[RulePack]:
    return load_yaml_dir_as(dir, RulePack)


def load_builtin_packs() -> list[RulePack]:
    return load_packs(_builtin_dir())
