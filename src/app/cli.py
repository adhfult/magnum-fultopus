"""Command-line entry point: `uv run app --help`."""

from __future__ import annotations

import argparse
import sys

from app import __version__
from app.config import Settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="app",
        description="A local-first, four-pillar computational research lab: chip thermals, AI on small hardware, astrophysics, and market monitoring, measured on my own machines.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="show settings and check the local model")
    sub.add_parser("models", help="list models available on the local AI server")

    ask = sub.add_parser("ask", help="ask the local model")
    ask.add_argument("prompt", help="what to ask")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = Settings.from_env()

    from app.llm import LocalModelError, generate, list_models

    try:
        if args.command == "status":
            print(f"magnum-fultopus {__version__}")
            print(f"data dir:     {settings.data_dir}")
            print(f"local model:  {settings.llm_model} at {settings.llm_base_url}")
            return 0
        if args.command == "models":
            for name in list_models(settings):
                print(name)
            return 0
        if args.command == "ask":
            print(generate(args.prompt, settings))
            return 0
    except LocalModelError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 2
