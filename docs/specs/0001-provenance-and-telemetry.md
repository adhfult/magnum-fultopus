# Spec: Provenance schema and telemetry exporter

- Status: draft (waiting for Adham's approval)
- Source: docs/CHARTER.md Parts 9.2 and 9.3; NOW.md week 0.

## Goal
Every measurement from every pillar is written in one row format, and a small
exporter records power, temperature and utilization from the PC and Pi into a
local cache. An experiment can then ask "what was the GPU drawing between
12:00:03 and 12:04:41?" and join that with its own results. Without this there
are no energy numbers (Pillar II) and nothing to fit thermal models to (Pillar I).

## User story
As Adham, I want every result and every sensor sample in one format so that I
can join them later without cleaning, and so that any number in the journal can
be traced to a commit, a machine and a config.

## The row format (the "schema")
One long-format row per measured value. Same columns for experiment results and
telemetry samples.

| Column | Meaning | Example |
|---|---|---|
| `ts_utc` | ISO 8601, UTC, with `Z` | `2026-10-12T14:03:07.250Z` |
| `machine` | `pc`, `laptop`, `pi400`, `colab` | `pc` |
| `run_id` | groups the rows of one run; empty for telemetry | `20261012T140300-llama-q4` |
| `git_commit` | short hash of this repo | `a1b2c3d` |
| `git_dirty` | `1` if the tree had uncommitted changes | `0` |
| `software` | JSON object of key versions | `{"python":"3.11.9","llama.cpp":"b4567"}` |
| `driver` | GPU driver version, empty if none | `Adrenalin 25.x` |
| `config` | JSON object of the run's settings | `{"quant":"Q4_K_M","ctx":2048}` |
| `metric` | what was measured | `tokens_per_s`, `gpu_power_w` |
| `value` | a number | `41.7` |
| `unit` | the unit, always filled | `tok/s`, `W`, `C`, `%` |

Why long format (one metric per row) and not one column per metric: new pillars
add new metrics without changing the schema, and joining telemetry onto a run is
a plain filter on `metric` and a time window.

## Storage (one decision for you)
- **Recommended for v1: CSV**, written with Python's `csv` module. Zero new
  dependencies, works on the Pi, readable in any editor. At 1 sample per second
  per sensor a day is about 86,000 rows per sensor, which is small.
- Alternative: parquet via `pyarrow`, which `AGENTS.md` mentions. It is smaller and
  faster to read, but it is a large dependency to carry on a 4 GB Pi for no gain
  at this size. Switching later is one function if reading ever gets slow.
- Layout: `data/telemetry/YYYY-MM-DD/<machine>.csv`, append-only, gitignored.
  Experiment results go to `results/` (committed) when they back a claim.

## Where the code goes
- `bench/provenance.py`: the `Row` definition, `capture_env()` (commit, dirty flag,
  versions), and a writer. Shared by every pillar.
- `telemetry/cache.py`: append samples, and `window(machine, metric, start, end)` to read.
- `telemetry/sources/`: one small module per sensor source (see below).
- `telemetry/exporter.py`: loop that polls the sources and appends rows.

## Sensor sources
| Machine | Source | Gives | Notes |
|---|---|---|---|
| PC (Windows side) | LibreHardwareMonitor | GPU power, GPU and CPU temperature, utilization | Exporter runs in WSL and reads LHM over localhost, so code and git stay in Ubuntu. LHM has a built-in web server option; **[verify the URL and JSON shape from LHM's docs or by running it, before writing the parser]** |
| Pi 400 | Linux sysfs and `/proc` (`thermal_zone0/temp`, cpufreq, meminfo, CPU stat) | `cpu_temp_c`, `cpu_util_pct`, `cpu_freq_mhz`, `mem_used_pct`, `mem_used_gb` | The old project measured exactly these on the Pi (see below). No power sensor, so **no Pi power** until a wall-plug meter exists. Do not invent a number. |
| Any Linux | same sources | same metrics | Used for tests and the laptop |

Keep the old metric names so old and new Pi data join without renaming.

## What is already known about the Pi
Source: old project `05_telemetry/analysis/FINDINGS.md` (closed out 21 Sep 2026, read 2026-10-11).
It logged 483,685 rows over about 27 days (roughly one sample per 5 s, from the row count).
- Idle the whole time: mean CPU utilization 0.79%, mean `cpu_temp_c` 36.81 C (min 31.15, max 43.33).
- No usable load-drop events, so **no thermal time constant exists yet**. Pillar I needs a deliberate step-load test on the Pi, not more idle logging.
- The exporter stopped on 21 Sep when the SD card was repurposed, so the Pi currently has no telemetry destination. This spec gives it one.
- The old parquet file is a comparison source, not something to copy code from. Importing it as history is optional and out of scope here.

## Acceptance criteria
- [ ] A `Row` with a missing column, a non-number value, or an empty unit is rejected with a clear error.
- [ ] `capture_env()` records the commit and sets `git_dirty` correctly (checked against a clean and a dirty temp repo).
- [ ] Writing rows then reading `window(...)` returns exactly the rows inside the time window, in time order.
- [ ] Restarting the exporter appends; it never overwrites or duplicates earlier rows.
- [ ] A missing sensor produces a logged gap, never a fake `0`.
- [ ] On the PC with LHM running: a 60 second run writes `gpu_power_w` samples that are not all zero. This one can only be checked by Adham on the real machine.

## Edge cases and errors
- LHM not running or unreachable: retry every few seconds, log one line per outage, keep the gap visible.
- Clock: always UTC. Local time never appears in the cache.
- Same timestamp twice (fast polling): both rows are kept; the reader does not dedupe silently.
- A partial last line after a crash: the reader skips it and reports it.

## Out of scope
- Plots and dashboards. Parquet. Deploying the exporter on the Pi (a later task, uses `deploy/pi/`).
- The `core/` SVD wrapper and hand-computed-case test helper (separate, next).
- Any power measurement for the Pi or laptop. The Pi step-load test (for the thermal time constant) is a Pillar I task, not part of this spec.

## Test plan
- Unit tests in `bench/` and `telemetry/` next to the code, using fake sources
  and temp directories. No hardware needed for CI.
- By hand, on the PC: start LibreHardwareMonitor, run the exporter for 60 seconds,
  confirm the file exists and `gpu_power_w` moves. Record the result in the journal
  with machine, commit and wall time.

## Build order (one small commit each)
1. `bench/provenance.py` and its tests.
2. `telemetry/cache.py` and its tests.
3. sysfs source and its tests.
4. LHM source, after the API is verified.
5. `telemetry/exporter.py`, then the by-hand PC check.
