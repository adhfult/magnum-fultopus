# magnum-fultopus

A local-first research lab built on one argument: computation is limited by
moving bytes and removing heat, and the mathematics that describes those limits
(linear algebra, partial differential equations, stochastic processes) is the
same mathematics that finds planets in noisy light curves and structure in noisy
markets. Four pillars (heat, bytes, stars, signals), measured on my own
machines. Full charter: `docs/CHARTER.md`.

## Run it
```bash
uv sync                  # install dependencies (first time)
cp .env.example .env     # optional: adjust settings
uv run app status
uv run app ask "hello"   # needs Ollama running locally (optional)
```

## Check it
```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

## Run it natively on Windows (only if it has to)
```bash
./scripts/run-windows.sh status   # needs uv on Windows (dotfiles\windows\setup-local-ai.ps1)
```

## Run it on the Raspberry Pi
See `deploy/pi/README.md`.

## Where things are
- `docs/CHARTER.md`, `docs/NOW.md`, `docs/JOURNAL.md`: charter, current fortnight, newest-first log
- `docs/PRODUCT.md`: what this is, who it's for, what it isn't
- `docs/ARCHITECTURE.md`: how it's built
- `docs/SECURITY.md`: project-specific security rules
- `docs/specs/`, `docs/decisions/`: feature specs and decision records
- `AGENTS.md`: instructions for AI coding agents
