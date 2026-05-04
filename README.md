# mcp-game-rules

MCP server exposing data-driven game rules for the **Fante RPG** — and any other
game built on the Fante stack.

The server resolves dice rolls, action checks, and effects against rule packs
loaded from YAML. Rule packs are layered, versioned, and tiered by complexity so
the ruleset can grow with the player.

## What this is for

Fante is a voice/text RPG built for Fernando's son to play with. The orchestrator
([`fante-game-orchestrator`](https://github.com/fermaat/fante-game-orchestrator))
needs a `RulesPort` adapter that does more than roll dice — it should resolve
typed actions ("climb the cliff", "cast a spark of light") against a ruleset that
the player and his dad can extend by editing YAML files together.

This repo is the **server side** of that contract: it loads rule packs, resolves
checks, and exposes them over MCP. The orchestrator-side `MCPRulesAdapter` lives
in the orchestrator repo.

## Stack

- Python 3.12, pdm
- [MCP](https://modelcontextprotocol.io) — Python SDK, stdio transport
- pydantic v2 — typed rule-pack model
- [`core-utils`](https://github.com/fermaat/core-utils) — settings, logger, YAML loader
- pyyaml, loguru

## Status

**Phase 2 complete.** Domain models, dice engine, condition evaluator, YAML loader,
`SystemChecker`, `CompositeRuleEngine`, and three built-in packs are in place.
94 tests, all green. See `docs/IMPLEMENTATION_PLAN.md` for the full phased plan.

**Next:** Phase 3 — MCP stdio server (`server.py`, `__main__.py`).

## Quick start (once Phase 1+ are done)

```bash
pdm install --dev
pdm run python -m mcp_game_rules           # boot the MCP server on stdio
./run_local_checks.sh                      # black + mypy + tests
```

## Repository layout

```
src/mcp_game_rules/
├── config.py                  # Settings (extra_pack_paths, autoload_builtin)
├── protocols.py               # DiceRoller, CheckResolver, RuleEngine protocols
├── domain/                    # Pydantic models — Actor, Attributes, DicePolicy, Rule, RulePack …
├── engine/                    # dice.py, conditions.py, checker.py, composite.py, format.py
└── packs/
    ├── loader.py              # load_pack / load_packs / load_builtin_packs
    └── builtin/               # physics_basic.yaml, magic_basic.yaml, environment_forest.yaml
tests/
├── unit/                      # 53 assertions — attributes, dice, conditions, format, packs
└── functional/                # 16 assertions — loader, checker, composite
docs/
├── IMPLEMENTATION_PLAN.md
└── PACK_AUTHORING.md          # how to write a YAML rule pack
```
