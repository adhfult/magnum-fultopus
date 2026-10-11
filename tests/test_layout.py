def test_namespace_packages_import():
    import bench
    import core
    import telemetry

    assert core and bench and telemetry
