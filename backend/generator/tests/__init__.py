import unittest


def load_tests(loader, tests, pattern):
    """Ładuje wszystkie moduły testowe jako jeden TestSuite."""
    suite = unittest.TestSuite()

    # --- Testy podstawowe (zawsze uruchamiane) ---
    from test_api import *

    core_modules = [
        test_cv_agent,
    ]

    for module in core_modules:
        suite.addTests(loader.loadTestsFromModule(module))

    return suite
