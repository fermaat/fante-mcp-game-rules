"""Phase 0 smoke test — package imports cleanly and exposes its version.

Replaced by real tests in Phase 1.
"""

import pytest

import mcp_game_rules


@pytest.mark.unit
def test_package_imports() -> None:
    assert mcp_game_rules.__version__ == "0.2.0"
