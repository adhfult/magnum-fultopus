from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_namespace_packages_resolve_to_repo():
    import bench
    import core
    import telemetry

    for pkg in (core, bench, telemetry):
        assert Path(pkg.__path__[0]).resolve() == ROOT / pkg.__name__
