"""Talk to a local AI model. Free, private, and no paid API keys.

Works with any server that speaks the common "OpenAI-compatible" chat format:
Ollama (default), LM Studio, llama.cpp's server, and others. Uses only the
standard library, so it adds no dependencies.

By default it only talks to this machine. Another machine on your home
network (e.g. the Pi borrowing a PC's model) is allowed only when
LLM_ALLOW_LAN / LOCAL_AI_ALLOW_LAN is set. Internet addresses are always refused.
"""

from __future__ import annotations

import ipaddress
import json
import urllib.error
import urllib.request
from urllib.parse import urlparse

from app.config import Settings


class LocalModelError(RuntimeError):
    """Raised when the local model can't be reached or returns an error."""


def check_url_allowed(url: str, allow_lan: bool) -> None:
    """Refuse anything that isn't this machine (or, if allowed, the home network)."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise LocalModelError(f"Not a valid server address: {url}")
    host = parsed.hostname
    if host in {"localhost", "127.0.0.1", "::1"}:
        return
    if allow_lan:
        if host.endswith(".local"):
            return
        try:
            if ipaddress.ip_address(host).is_private:
                return
        except ValueError:
            pass
        raise LocalModelError(f"{host} isn't on your home network; only local models are allowed.")
    raise LocalModelError(
        f"{host} isn't this machine. To use another machine on your home network, "
        "set LLM_ALLOW_LAN=1 (or run local-ai-profile.sh --remote)."
    )


def _request(settings: Settings, path: str, body: dict | None, timeout: float) -> dict:
    check_url_allowed(settings.llm_base_url, settings.llm_allow_lan)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = urllib.request.Request(  # noqa: S310 (address checked above)
        f"{settings.llm_base_url}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            return json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300]
        raise LocalModelError(f"Model server error {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise LocalModelError(
            f"Couldn't reach the model server at {settings.llm_base_url}. Is Ollama running?"
        ) from exc


def chat(
    messages: list[dict[str, str]], settings: Settings | None = None, timeout: float = 300
) -> str:
    """Send a conversation ([{"role": "user", "content": "..."}]) and return the reply."""
    settings = settings or Settings.from_env()
    payload = _request(
        settings,
        "/chat/completions",
        {"model": settings.llm_model, "messages": messages, "stream": False},
        timeout,
    )
    try:
        return str(payload["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise LocalModelError(f"Unexpected reply from the model server: {payload}") from exc


def generate(prompt: str, settings: Settings | None = None, timeout: float = 300) -> str:
    """Ask a single question and return the answer."""
    return chat([{"role": "user", "content": prompt}], settings, timeout)


def list_models(settings: Settings | None = None, timeout: float = 10) -> list[str]:
    """Names of the models available on the server."""
    settings = settings or Settings.from_env()
    payload = _request(settings, "/models", None, timeout)
    return [m.get("id", "") for m in payload.get("data", [])]
