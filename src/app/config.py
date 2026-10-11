"""Settings, read from environment variables (and a local .env file if present).

Where the local AI settings come from, first match wins:
1. This project's .env (LLM_BASE_URL, LLM_MODEL, LLM_ALLOW_LAN)
2. The machine profile written by ~/dotfiles/scripts/local-ai-profile.sh
   (LOCAL_AI_URL, LOCAL_AI_MODEL, LOCAL_AI_ALLOW_LAN)
3. Defaults: Ollama on this machine, with a model sized to this machine's RAM
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_LLM_URL = "http://localhost:11434/v1"


def load_dotenv(path: Path = Path(".env")) -> None:
    """Load KEY=VALUE lines from a .env file without overriding real env vars."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def total_ram_gb() -> int:
    """Total RAM of this machine in GB (0 if unknown). Works on Linux and Windows."""
    if sys.platform == "win32":
        import ctypes

        class MemoryStatus(ctypes.Structure):
            _fields_ = [  # noqa: RUF012 (ctypes layout)
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MemoryStatus()
        status.dwLength = ctypes.sizeof(MemoryStatus)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return int(status.ullTotalPhys // (1024**3))
        return 0
    try:
        with open("/proc/meminfo", encoding="utf-8") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    return int(line.split()[1]) // (1024 * 1024)
    except OSError:
        pass
    return 0


def model_for_ram(ram_gb: int) -> str:
    """A reasonable default model for the given amount of RAM (Ollama tags)."""
    if ram_gb >= 24:
        return "qwen3:30b-a3b"  # mixture-of-experts: strong and still fast on CPU
    if ram_gb >= 12:
        return "qwen3:8b"
    if ram_gb >= 6:
        return "qwen3:4b"
    return "qwen3:1.7b"


def _first(*names: str) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


@dataclass(frozen=True)
class Settings:
    llm_base_url: str = DEFAULT_LLM_URL
    llm_model: str = "qwen3:8b"
    llm_allow_lan: bool = False
    data_dir: Path = Path("data")

    @classmethod
    def from_env(cls) -> Settings:
        load_dotenv()
        allow = _first("LLM_ALLOW_LAN", "LOCAL_AI_ALLOW_LAN") or "0"
        return cls(
            llm_base_url=(_first("LLM_BASE_URL", "LOCAL_AI_URL") or DEFAULT_LLM_URL).rstrip("/"),
            llm_model=_first("LLM_MODEL", "LOCAL_AI_MODEL") or model_for_ram(total_ram_gb()),
            llm_allow_lan=allow.lower() in {"1", "true", "yes"},
            data_dir=Path(os.environ.get("DATA_DIR", "data")),
        )
