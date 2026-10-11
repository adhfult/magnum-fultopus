# 0001: Pillar IV is a market monitor first

- Date: 2026-10-11
- Status: accepted

## Context
Charter Part 8 framed Pillar IV as quantum and quantitative trading research.
Adham wants a market monitor for now, not a trader. A monitor already exists:
Adham's fork github.com/adhfult/tradingview-mcp (local checkout
`~/code/tradingview-mcp`, working branch `claude/lucid-bardeen-3ou62p`). It has
read-only market data tools, backtests, and a watcher (in progress) with alert
rules, a local API and a systemd unit example for the Pi (not deployed yet).
It runs standalone. Charter Part 15 Q3 asked
whether such a project should live in this repo or stay separate.

## Decision
- Pillar IV is a market monitor for now, using tradingview-mcp.
- tradingview-mcp stays a separate repo (answers Part 15 Q3). Claude sessions
  here reach it through `.mcp.json`.
- Quantum, QUBO and QAOA work is deferred.
- No trading or signal logic in this repo. The rule "paper/backtest only" is
  unchanged.

## Alternatives considered
- Copy the monitor into this repo: breaks "each tool is standalone in its own
  repo" and duplicates code that already runs.
- Keep the quantum scope: no working quantum code exists, and the monitor is
  useful now.

## Consequences
- Easier: the monitor and its planned Pi service keep evolving in their own repo.
- Known gap: tradingview-mcp caches only in memory (60 s TTL), not on disk.
  Charter rule 3 wants every pull cached to disk. Future task.
- GitHub `main` of that fork is behind (v0.9.0: no watcher, no `tv_*` tools).
  Pointers name the local branch, which is v0.10.0.
- `p4_quant/qubo/` and `p4_quant/qaoa/` are removed. Re-add them if quantum
  work comes back.
