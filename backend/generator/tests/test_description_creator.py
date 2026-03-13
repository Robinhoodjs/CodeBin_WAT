import unittest
import os
import sys

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "src")))

from description_creator import story_teller, task_describer, names_creator


class TestStoryTeller(unittest.TestCase):
    """Tests for story_teller()"""

    def test_is_callable(self):
        self.assertTrue(callable(story_teller))

    def test_returns_none(self):
        """Current stub implementation should return None."""
        self.assertIsNone(story_teller())

    def test_accepts_no_arguments(self):
        try:
            story_teller()
        except TypeError:
            self.fail("story_teller() raised TypeError unexpectedly")

    def test_has_docstring(self):
        self.assertIsNotNone(story_teller.__doc__)
        self.assertIn("tale", story_teller.__doc__)


class TestTaskDescriber(unittest.TestCase):
    """Tests for task_describer()"""

    def test_is_callable(self):
        self.assertTrue(callable(task_describer))

    def test_returns_none(self):
        self.assertIsNone(task_describer())

    def test_accepts_no_arguments(self):
        try:
            task_describer()
        except TypeError:
            self.fail("task_describer() raised TypeError unexpectedly")

    def test_has_docstring(self):
        self.assertIsNotNone(task_describer.__doc__)
        self.assertIn("task", task_describer.__doc__)


class TestNamesCreator(unittest.TestCase):
    """Tests for names_creator()"""

    def test_is_callable(self):
        self.assertTrue(callable(names_creator))

    def test_returns_none(self):
        self.assertIsNone(names_creator())

    def test_accepts_no_arguments(self):
        try:
            names_creator()
        except TypeError:
            self.fail("names_creator() raised TypeError unexpectedly")

    def test_has_docstring(self):
        self.assertIsNotNone(names_creator.__doc__)
        self.assertIn("names", names_creator.__doc__)


if __name__ == "__main__":
    unittest.main()
