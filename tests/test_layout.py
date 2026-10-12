from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_namespace_packages_resolve_to_repo():
    import bench
    import core
    import telemetry

    for pkg in (core, bench, telemetry):
        assert Path(pkg.__path__[0]).resolve() == ROOT / pkg.__name__


def test_packages_import_outside_pytest(tmp_path):
    """pytest's pythonpath setting hides a broken install, so check a fresh interpreter."""
    import subprocess
    import sys

    code = "import bench, core, telemetry"
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-I", "-c", code], cwd=tmp_path, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
