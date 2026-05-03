from pathlib import Path

from core_utils.settings import CoreSettings


class Settings(CoreSettings):
    """mcp-game-rules settings.

    Pack search order: `extra_pack_paths` → `~/.fante/packs/` → builtin.
    """

    extra_pack_paths: list[Path] = []
    autoload_builtin: bool = True
