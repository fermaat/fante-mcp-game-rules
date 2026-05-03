"""Pytest configuration and shared fixtures."""

import os
from pathlib import Path

import pytest

os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("LOG_LEVEL", "DEBUG")


@pytest.fixture(scope="session")
def project_root() -> Path:
    return Path(__file__).parent.parent


class FakeRng:
    """Deterministic RNG: yields a fixed sequence of ints from randint."""

    def __init__(self, sequence: list[int]) -> None:
        self._sequence = list(sequence)

    def randint(self, a: int, b: int) -> int:
        return self._sequence.pop(0)
