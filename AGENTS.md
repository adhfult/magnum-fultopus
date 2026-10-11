# magnum-fultopus

A local-first, four-pillar computational research lab: chip thermals, AI on small hardware, astrophysics, and market monitoring, measured on my own machines.

Four pillars: (I) thermodynamics & microchip engineering, (II) AI hardware &
small-memory models, (III) computational astrophysics & instrumentation,
(IV) quantitative markets: monitoring first, quantum deferred. One thesis: computation is limited
by moving bytes and removing heat; the same maths (SVD, PDEs, stochastic
processes, optimization) runs through all four. Full charter: docs/CHARTER.md.

Instructions for every AI coding agent working in this repo (Claude Code reads
this through CLAUDE.md; Antigravity, Copilot and Codex read it directly).

**This is a local-first project:** it runs free on my own machines, with no
paid APIs, cloud AI, or hosted servers (see "Local-first tools" in my global rules).

## Stack
- Python 3.11+ managed with uv (`pyproject.toml`, `uv.lock`)
- Code in `src/app/`, tests in `tests/` (pytest), linting/formatting with ruff
- Runs locally on WSL or the Raspberry Pi (64-bit ARM). No paid services
  and no hosted servers unless docs/ARCHITECTURE.md says otherwise.
- Local AI through `src/app/llm.py`: any OpenAI-compatible server on this
  machine (Ollama by default; LM Studio, llama.cpp also work). Never a paid API
  key or a cloud model. Model and server come from the machine profile
  (`LOCAL_AI_*`) unless this project's `.env` overrides them.

## Commands
- `uv run app --help`: run the tool
- `uv run pytest`: tests
- `uv run ruff check . && uv run ruff format --check .`: lint and format check
- `uv run ruff format .`: auto-format
- Run tests and ruff before saying work is done.

## Starting from scratch
This project does not import, copy or extend code from the old
"The Study of Important Things/research-lab" repo. That repo is archived,
read-only context: its findings (docs/CHARTER.md Part 4) inform decisions, and
its outputs may be used as a comparison check *after* new code is written.
Don't suggest porting old modules.

## Before starting any session
1. Read docs/NOW.md and the top of docs/JOURNAL.md.
2. Run `git log --oneline -15` and `git status`. Don't redo finished work; don't
   touch another session's uncommitted files without asking.
3. Read `docs/PRODUCT.md` (what we're building and what we're NOT building).
   The charter docs (docs/CHARTER.md, NOW.md) take priority over PRODUCT.md.
4. For a new feature, read or write its spec in `docs/specs/` first (copy
   `docs/specs/TEMPLATE.md`). If there's no spec, propose one and wait for approval.

## Who writes what
- Adham writes by hand: solvers, attention/model architecture, prediction
  models, trading strategy/signal logic, QUBO formulations. Claude may scaffold
  with clearly marked blanks, explain, and review, but not fill these in.
- Claude may write: harnesses, plumbing, data pulls, plotting, tests, CI,
  benchmarks, docs for code that exists.

## Rules
- Code meant for the Raspberry Pi must use pure-Python dependencies or ones
  with arm64 wheels and fit its 4 GB (Raspberry Pi 400). Experiments state
  which machine they ran on. Target 8 GB PCs as the minimum for PC tools.
- Prompts must work with small local models: be explicit, give examples, ask
  for simple output formats (plain text or small JSON), and validate replies.
- This tool is standalone: its own repo, its own copy of llm.py, no shared
  service it depends on besides the local model server.
- Add dependencies with `uv add <package>` (never pip install into the system).
- Secrets and settings live in `.env` (never committed); names go in `.env.example`.
- Network services bind to 127.0.0.1 unless a decision record says otherwise.
- Record significant decisions in `docs/decisions/`.
- Before sharing or deploying, run the pre-ship-security skill against `docs/SECURITY.md`.
- Exception to local-first: tools stay local-first; free Colab/Kaggle notebooks
  only for CUDA-only training/quantization, run by hand, never a runtime dependency.
- Label every command with its machine: PC (sim-server: Ryzen 7600X, RX 570 8GB,
  Vulkan only, no CUDA/ROCm), laptop, Pi 400, or Colab/Kaggle.
- A run you didn't log didn't happen: config, versions/commits, hardware,
  results with units, wall time. Numbers, not adjectives.
- Verify before asserting. Specs, papers, connector data: cite source and
  retrieval date, cache to disk. Never type a spec from memory.
- Measure before optimizing; log before/after.
- Every result has a baseline (PID, same-size off-the-shelf model, SPY after
  costs, simulated annealing). Publish losses too.
- Trading is paper/backtest only. No live orders, no order-placing brokerage
  connections. Read-only data is fine.
- No secrets in chat or git. If a key appears, say it needs rotating.
- Running code beats more documents.

## Where it runs
Code is always written and committed in Ubuntu (WSL). When it runs, prefer,
in this order:
1. **Inside Ubuntu / on the Pi** (default).
2. **Ubuntu talking to a Windows app over localhost**: emulator scripting or
   network APIs, OBS's remote control, Roblox Studio via Rojo, Ollama.
   Mirrored networking makes localhost work both ways.
3. **Natively on Windows** only when it must, such as reading another Windows
   program's memory or Windows-only libraries: `./scripts/run-windows.sh <args>`
   runs this same folder on Windows with its own separate environment. Code
   that must work there avoids Linux-only paths and commands (use `pathlib`).

## Layout
- `src/app/cli.py`: command-line entry point
- `src/app/config.py`: settings from environment / .env
- `src/app/llm.py`: local AI helper (`chat`, `generate`, `list_models`)
- `deploy/pi/`: systemd service + timer for running on the Pi
- `scripts/run-windows.sh` / `.ps1`: run natively on Windows when needed
- `docs/`: charter, NOW, JOURNAL, product, architecture, security, decisions, specs
- `docs/sources/`: cached papers' metadata, spec sheets, retrieval dates
- `core/`: shared math library + tests
- `bench/`: provenance schema, harnesses, optimizer sweeps
- `telemetry/`: exporter + cache reader
- `p1_thermal/`, `p2_ai_hw/`, `p3_astro/`, `p4_quant/`: one folder per pillar
  (subfolders per charter Part 10)
- `results/`: committed CSVs + PNGs that back public claims

## Hardware facts (measured, don't re-derive)
- RX 570: 7.75 GB device-local VRAM via Vulkan; 224 GB/s; inference only.
- Training / CUDA-only quantization → Colab/Kaggle T4.
- Telemetry: exporter → parquet cache; GPU power via LibreHardwareMonitor on Windows.
