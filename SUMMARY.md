# mcp-game-rules — Summary

## Purpose
MCP server exposing data-driven game rules for the Fante RPG. Loads rule packs from YAML,
resolves dice rolls and action checks, and exposes them via the MCP stdio protocol. Built
so Fernando's son can play a growing RPG with rules that dad can extend by editing YAML files.

## Architecture tree

```
src/mcp_game_rules/
├── __init__.py                 # version + public re-exports
├── __main__.py                 # `python -m mcp_game_rules` → boot stdio server
├── server.py                   # FastMCP server: 4 tools + rule-pack resource template
├── config.py                   # Settings (extra_pack_paths, autoload_builtin)
├── protocols.py                # DiceRoller, CheckResolver, RuleEngine (Protocol classes)
├── domain/
│   ├── attributes.py           # Attribute (StrEnum), Attributes (0–8 per attr), .get()
│   ├── actor.py                # Actor(name, attributes, skills, tags)
│   ├── dice.py                 # DicePolicy (d20s/keep/plot_dice), PlotDieFace
│   ├── results.py              # RollResult, AppliedModifier, CheckResult
│   ├── effects.py              # Effect(name, magnitude, duration_turns) — declared, not auto-applied
│   ├── conditions.py           # Condition(field, op, value) — structured DSL
│   └── pack.py                 # Modifier, Rule, RulePack (with unique-id validator)
├── engine/
│   ├── dice.py                 # SystemDice — DicePolicy executor + spec rolls + plot dice
│   ├── format.py               # pretty_rule(rule, pack_default_policy) → str
│   ├── conditions.py           # evaluate(condition, scope) → bool  [Phase 2]
│   ├── checker.py              # SystemChecker — resolves check against a rule  [Phase 2]
│   └── composite.py            # CompositeRuleEngine — owns loaded packs; from_settings() factory
└── packs/
    ├── loader.py               # load_pack / load_packs / load_builtin_packs  [Phase 2]
    └── builtin/
        ├── physics_basic.yaml  # tier 1, physical — climb, dodge, swim, lift  [Phase 2]
        ├── magic_basic.yaml    # tier 2, magical — spark, mend, push  [Phase 2]
        └── environment_forest.yaml  # tier 1, environmental — path, forage, weather  [Phase 2]

tests/
├── conftest.py                 # ENV setup, FakeRng (deterministic dice)
├── unit/                       # Phase 1 tests (53 assertions, all passing)
├── functional/                 # Phase 2 tests — loader, checker, composite  [Phase 2]
└── integration/                # Phase 3 ✓ — spawns real MCP subprocess (5 tests)
```

## Key classes / functions

| Name | Location | What it does |
|---|---|---|
| `Attribute` | `domain/attributes.py` | StrEnum: strength/speed/intellect/willpower/awareness/presence |
| `Attributes` | `domain/attributes.py` | Pydantic model, 0–8 per attr, `.get(attr)` |
| `Actor` | `domain/actor.py` | name + Attributes + skills dict + tags list |
| `DicePolicy` | `domain/dice.py` | d20s, keep (highest/lowest/all), plot_dice |
| `PlotDieFace` | `domain/dice.py` | OPPORTUNITY / COMPLICATION / BLANK |
| `RollResult` | `domain/results.py` | spec, total, breakdown; `__str__` → "2d6+3 → [4+2+3] = 9" |
| `CheckResult` | `domain/results.py` | full resolution output: rolls, bonuses, modifiers, success |
| `Condition` | `domain/conditions.py` | field (dot-path), op, value — structured modifier DSL |
| `Rule` / `RulePack` | `domain/pack.py` | Rule definition and collection; RulePack validates unique IDs |
| `SystemDice` | `engine/dice.py` | `roll_spec(spec)`, `execute_policy(policy)` — injectable RNG |
| `pretty_rule` | `engine/format.py` | Human-readable rule dump for logs and `describe_rule` |

## Main entry points

```python
from mcp_game_rules import CompositeRuleEngine, Actor, Attributes, Attribute, DicePolicy

# Load builtin packs and run a check
engine = CompositeRuleEngine.from_settings()
actor = Actor(name="Fante", attributes=Attributes(strength=2, speed=3), skills={"athletics": 1})
result = engine.check("climb", actor, context={"surface": "wet"})
print(result.success, result.total)
```

Boot as MCP server:
```bash
python -m mcp_game_rules      # stdio transport
```

## Configuration

| Var / Field | Default | Purpose |
|---|---|---|
| `ENVIRONMENT` | `development` | passed to CoreSettings |
| `LOG_LEVEL` | `INFO` | loguru level |
| `extra_pack_paths` | `[]` | additional YAML pack directories |
| `autoload_builtin` | `True` | load `packs/builtin/` on boot |

## Dependencies

| Package | Purpose |
|---|---|
| `mcp` | MCP Python SDK, stdio transport |
| `pydantic` v2 | typed models for domain + rule packs |
| `pydantic-settings` | Settings class |
| `core-utils` (git) | CoreSettings, YAML loader utilities |
| `pyyaml` | YAML parsing |
| `loguru` | structured logging |

Dev: `pytest`, `pytest-cov`, `pytest-asyncio`, `black`, `ruff`, `mypy`, `isort`, `types-PyYAML`

## Phase / status

- **Phase 0** ✓ Bootstrap — deps, tooling, plan locked
- **Phase 1** ✓ Domain models, protocols, dice engine, unit tests (53 assertions, all green)
- **Phase 2** ✓ YAML loader, condition engine, checker, built-in packs (94 tests total, all green)
- **Phase 3** ✓ MCP stdio server (`server.py`, `__main__.py`) — 99 tests total (5 integration)
- **Phase 4** — ecosystem update (repos_index, fante-game-orchestrator unblock)

## Consumers / upstream

- **Upstream:** `core-utils` (settings + YAML loader)
- **Consumer:** `fante-game-orchestrator` — will add an `MCPRulesAdapter` that talks to this
  server over stdio. Adapter lives in the orchestrator repo, not here.
- MCP protocol is the integration boundary; no shared Python types cross the boundary.

## Out of scope for v0.1

Persistent effect tracking, multi-actor checks, runtime pack reload, MCP `prompts`,
auth/multi-user, skill auto-derivation.
