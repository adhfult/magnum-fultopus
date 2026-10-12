# Journal

Newest first. Each entry: what was built and run, the numbers, what it means
(physics/maths written out so it can be copied into the paper notebook), and
the wrong turns. (Charter Part 9.4.)

## 2026-10-11: Setup and Pillar IV reframe

**Built:** pytest and ruff wired so tests can live next to code in `core/`, `bench/`, `telemetry/` and the pillar folders, plus `tests/test_layout.py`. Pillar IV is now monitor-first via tradingview-mcp (decision 0001); quantum/QUBO deferred; `.mcp.json` added.

The old `study-of-important-things` repo (the archived research-lab) was set read-only on GitHub; the Pi stock station can still pull from it.

**Run:** PC/WSL. `uv run pytest`: 14 passed before, 15 after. `ruff check` and `ruff format --check` clean.

**Wrong turns:** the Dependabot PR (ruff 0.16.10) was merged after local checks because GitHub Actions jobs did not start (account billing/spending limit; private repo).

## 2026-10-11: Founding

**Built:** repo created locally from `template-local`; charter copied to
`docs/CHARTER.md`; Part 10 folder layout created (empty folders with `.gitkeep`);
AGENTS.md merged with the Part 12 working agreements.

**Run:** nothing yet. No experiments, no measurements, no numbers.

**Wrong turns:** deleting the template clone's `.git` was blocked by a safety check, so the template files were exported with `git archive` instead.
