import io
import json

import pytest

from app import llm
from app.config import Settings


def fake_server(reply: dict, seen: list):
    def fake_urlopen(request, timeout):
        seen.append(request)
        return io.BytesIO(json.dumps(reply).encode())

    return fake_urlopen


def test_generate_uses_openai_compatible_chat(monkeypatch):
    seen = []
    reply = {"choices": [{"message": {"content": " hi there "}}]}
    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_server(reply, seen))
    assert llm.generate("hello", Settings(llm_model="m")) == "hi there"
    assert seen[0].full_url == "http://localhost:11434/v1/chat/completions"
    body = json.loads(seen[0].data)
    assert body["model"] == "m" and body["messages"][0]["content"] == "hello"


def test_list_models(monkeypatch):
    reply = {"data": [{"id": "qwen3:8b"}, {"id": "qwen3:4b"}]}
    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_server(reply, []))
    assert llm.list_models(Settings()) == ["qwen3:8b", "qwen3:4b"]


@pytest.mark.parametrize("url", ["https://api.example.com/v1", "http://8.8.8.8:11434/v1"])
def test_internet_addresses_always_refused(url):
    for allow in (False, True):
        with pytest.raises(llm.LocalModelError):
            llm.check_url_allowed(url, allow_lan=allow)


@pytest.mark.parametrize("url", ["http://192.168.1.50:11434/v1", "http://gamer15.local:11434/v1"])
def test_home_network_only_when_allowed(url):
    with pytest.raises(llm.LocalModelError):
        llm.check_url_allowed(url, allow_lan=False)
    llm.check_url_allowed(url, allow_lan=True)


def test_localhost_always_allowed():
    llm.check_url_allowed("http://localhost:11434/v1", allow_lan=False)
    llm.check_url_allowed("http://127.0.0.1:1234/v1", allow_lan=False)
