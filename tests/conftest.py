def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (e.g. talking to Notion) (deselect with '-m \"not slow\"')",
    )
