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

**Phase 0 — bootstrap.** Package renamed, deps declared, implementation plan
locked in `docs/IMPLEMENTATION_PLAN.md`. No domain code yet.

See `docs/IMPLEMENTATION_PLAN.md` for the phased build-out.

## Quick start (once Phase 1+ are done)

```bash
pdm install --dev
pdm run python -m mcp_game_rules           # boot the MCP server on stdio
./run_local_checks.sh                      # black + mypy + tests
```

## Repository layout

Until Phase 1 lands, the tree is just the template skeleton:

```
src/mcp_game_rules/   # package (currently a placeholder __init__.py)
tests/                # unit/ and integration/ subfolders
docs/IMPLEMENTATION_PLAN.md
```

The target tree is documented in the implementation plan.
