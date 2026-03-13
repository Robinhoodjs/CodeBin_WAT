import unittest


def load_tests(loader, tests, pattern):
    """Ładuje wszystkie moduły testowe jako jeden TestSuite."""
    suite = unittest.TestSuite()

    import test_utils
    import test_controller
    import test_description_creator
    import test_input_reader
    import test_output_describer

    test_modules = [
        test_utils,
        test_controller,
        test_description_creator,
        test_input_reader,
        test_output_describer,
    ]

    for module in test_modules:
        suite.addTests(loader.loadTestsFromModule(module))

    return suite
