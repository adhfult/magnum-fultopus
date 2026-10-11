from app.cli import main


def test_status_runs(capsys):
    assert main(["status"]) == 0
    assert "local model" in capsys.readouterr().out


def test_ask_reports_missing_model(monkeypatch, capsys):
    import app.llm as llm

    def fail(*_args, **_kwargs):
        raise llm.LocalModelError("not running")

    monkeypatch.setattr(llm, "generate", fail)
    assert main(["ask", "hello"]) == 1
    assert "not running" in capsys.readouterr().err
