# Architecture: magnum-fultopus

> Keep this current. Agents read it to understand how the pieces fit.

## Stack
| Layer | Choice | Where |
|---|---|---|
| Language | Python 3.11+, managed by uv | `pyproject.toml` |
| Entry point | argparse CLI (`uv run app`) | `src/app/cli.py` |
| Settings | environment variables / `.env` | `src/app/config.py` |
| Local AI | OpenAI-compatible server on this machine (Ollama by default) | `src/app/llm.py` |
| Tests / lint | pytest / ruff | `tests/`, `pyproject.toml` |
| Runs on | WSL and Raspberry Pi (arm64); systemd timer on the Pi | `deploy/pi/` |

## Settings
| Variable | Purpose | Default |
|---|---|---|
| `LLM_BASE_URL` | Local AI server for this project | machine's `LOCAL_AI_URL`, else `http://localhost:11434/v1` |
| `LLM_MODEL` | Model for this project | machine's `LOCAL_AI_MODEL`, else sized to RAM |
| `LLM_ALLOW_LAN` | Allow a model server elsewhere on the home network | machine's `LOCAL_AI_ALLOW_LAN`, else off |
| `DATA_DIR` | Where the tool stores files (gitignored) | `data` |

Model sizes by RAM (default Ollama tags): under 6 GB `qwen3:1.7b`, 6-12 GB
`qwen3:4b`, 12-24 GB `qwen3:8b`, 24 GB+ `qwen3:30b-a3b`.

Add every new variable here and to `.env.example`.

## Data
What the tool stores, where (`DATA_DIR`), and for how long.

## External inputs
Websites, APIs, devices, or files the tool reads, with any limits or terms.
