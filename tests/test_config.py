from app.config import Settings, load_dotenv, model_for_ram

ALL_KEYS = [
    "LLM_BASE_URL",
    "LLM_MODEL",
    "LLM_ALLOW_LAN",
    "LOCAL_AI_URL",
    "LOCAL_AI_MODEL",
    "LOCAL_AI_ALLOW_LAN",
    "DATA_DIR",
]


def clear(monkeypatch):
    for key in ALL_KEYS:
        monkeypatch.delenv(key, raising=False)


def test_env_file_does_not_override_real_env(tmp_path, monkeypatch):
    clear(monkeypatch)
    env_file = tmp_path / ".env"
    env_file.write_text("LLM_MODEL=from-file\n# comment\nDATA_DIR=/tmp/x\n")
    monkeypatch.setenv("LLM_MODEL", "from-env")
    load_dotenv(env_file)
    settings = Settings.from_env()
    assert settings.llm_model == "from-env"
    assert str(settings.data_dir) == "/tmp/x"


def test_project_settings_beat_machine_profile(monkeypatch):
    clear(monkeypatch)
    monkeypatch.setenv("LOCAL_AI_MODEL", "machine-model")
    monkeypatch.setenv("LOCAL_AI_URL", "http://localhost:1234/v1/")
    assert Settings.from_env().llm_model == "machine-model"
    assert Settings.from_env().llm_base_url == "http://localhost:1234/v1"
    monkeypatch.setenv("LLM_MODEL", "project-model")
    assert Settings.from_env().llm_model == "project-model"


def test_lan_off_by_default(monkeypatch):
    clear(monkeypatch)
    assert Settings.from_env().llm_allow_lan is False
    monkeypatch.setenv("LOCAL_AI_ALLOW_LAN", "1")
    assert Settings.from_env().llm_allow_lan is True


def test_model_tiers():
    assert model_for_ram(4) == "qwen3:1.7b"
    assert model_for_ram(8) == "qwen3:4b"
    assert model_for_ram(16) == "qwen3:8b"
    assert model_for_ram(32) == "qwen3:30b-a3b"


def test_total_ram_is_detected_here():
    from app.config import total_ram_gb

    assert total_ram_gb() >= 0
