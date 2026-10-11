# magnum-fultopus

A local-first, four-pillar computational research lab: chip thermals, AI on small hardware, astrophysics, and quantum/quant trading research, measured on my own machines.

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

## Before building anything
1. Read `docs/PRODUCT.md` (what we're building and what we're NOT building).
2. For a new feature, read or write its spec in `docs/specs/` first (copy
   `docs/specs/TEMPLATE.md`). If there's no spec, propose one and wait for approval.

## Rules
- Must run on the Raspberry Pi: pure-Python dependencies or ones with arm64
  wheels; keep memory use modest. Target 8 GB PCs as the minimum;
  anything meant for the Pi must fit its 4 GB (Raspberry Pi 400).
- Prompts must work with small local models: be explicit, give examples, ask
  for simple output formats (plain text or small JSON), and validate replies.
- This tool is standalone: its own repo, its own copy of llm.py, no shared
  service it depends on besides the local model server.
- Add dependencies with `uv add <package>` (never pip install into the system).
- Secrets and settings live in `.env` (never committed); names go in `.env.example`.
- Network services bind to 127.0.0.1 unless a decision record says otherwise.
- Record significant decisions in `docs/decisions/`.
- Before sharing or deploying, run the pre-ship-security skill against `docs/SECURITY.md`.

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
- `docs/`: product, architecture, security, decisions, specs
