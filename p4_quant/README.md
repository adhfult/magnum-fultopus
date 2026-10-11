# p4_quant: Pillar IV, market monitoring first

Pillar IV is a market monitor for now. Quantum work is deferred
(see docs/decisions/0001-pillar-iv-monitor-first.md). Paper/backtest only.

## The monitor
- Repo: github.com/adhfult/tradingview-mcp (my fork), local checkout
  `~/code/tradingview-mcp`, branch `claude/lucid-bardeen-3ou62p`. GitHub `main`
  is behind that branch.
- Its watcher serves a local API on 127.0.0.1:8787 (`/health`).

## Querying it from here
- Claude sessions in this repo load the `tradingview` server from `.mcp.json`.
- Public-data tools work without setup.
- The `tv_*` tools need Node, the bridge, and cookies in that repo's own
  settings file (see its README).

## Folders
- `data/`: cached pulls (gitignored)
- `validation/`: walk-forward and out-of-sample checks
- `classical/`: classical baselines
- `results/`: committed CSVs and PNGs that back claims
