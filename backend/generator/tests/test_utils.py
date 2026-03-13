import unittest
from unittest.mock import MagicMock, patch, PropertyMock
import sys
import os

# ---------------------------------------------------------------------------
# Mock heavy third-party dependencies BEFORE importing the module under test
# so that import-time side effects (ChatOpenAI instantiation, env-var prompts,
# TavilySearch, PythonREPL) are neutralised.
# ---------------------------------------------------------------------------

# Patch getpass so _set_if_undefined never blocks
_getpass_patcher = patch("getpass.getpass", return_value="fake-key")
_getpass_patcher.start()

# Ensure env vars exist so getpass is not even attempted
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("TAVILY_API_KEY", "test-key")

# Mock heavyweight imports
sys.modules.setdefault("langchain_openai", MagicMock())
sys.modules.setdefault("langchain_tavily", MagicMock())
sys.modules.setdefault("langchain_experimental", MagicMock())
sys.modules.setdefault("langchain_experimental.utilities", MagicMock())
sys.modules.setdefault("dotenv", MagicMock())
sys.modules.setdefault("langgraph", MagicMock())
sys.modules.setdefault("langgraph.graph", MagicMock())
sys.modules.setdefault("langgraph.types", MagicMock())
sys.modules.setdefault("langchain_core", MagicMock())
sys.modules.setdefault("langchain_core.messages", MagicMock())

# We need a real END sentinel — use a simple string
_mock_langgraph_graph = sys.modules["langgraph.graph"]
_mock_langgraph_graph.END = "__end__"

# Now we can safely import the functions under test by loading the module
# directly (it uses relative imports via __init__, so we load the file).
import importlib.util

_utils_path = os.path.join(
    os.path.dirname(__file__), os.pardir, "src", "utils.py"
)
_spec = importlib.util.spec_from_file_location("generator_utils", os.path.abspath(_utils_path))
_utils_mod = importlib.util.module_from_spec(_spec)

# Inject the mocked END into the module's namespace before exec
_utils_mod.END = "__end__"
# Provide stubs for names the module expects from imports
_utils_mod.ChatOpenAI = MagicMock()
_utils_mod.load_dotenv = MagicMock()
_utils_mod.BaseMessage = MagicMock()
_utils_mod.MessagesState = MagicMock()
_utils_mod.TavilySearch = MagicMock()
_utils_mod.PythonREPL = MagicMock()
_utils_mod.getpass = MagicMock()
_utils_mod.os = os

_spec.loader.exec_module(_utils_mod)

get_next_node = _utils_mod.get_next_node
should_continue = _utils_mod.should_continue
make_system_prompt = _utils_mod.make_system_prompt
END = "__end__"


# ============================= TESTS ======================================


class TestGetNextNode(unittest.TestCase):
    """Tests for get_next_node(last_message, goto)"""

    def _make_message(self, content: str):
        msg = MagicMock()
        msg.content = content
        return msg

    def test_returns_end_when_final_answer_present(self):
        msg = self._make_message("FINAL ANSWER: The result is 42.")
        result = get_next_node(msg, "text_corrector")
        self.assertEqual(result, END)

    def test_returns_goto_when_no_final_answer(self):
        msg = self._make_message("I need more information to proceed.")
        result = get_next_node(msg, "text_corrector")
        self.assertEqual(result, "text_corrector")

    def test_final_answer_at_start(self):
        msg = self._make_message("FINAL ANSWER")
        self.assertEqual(get_next_node(msg, "next_node"), END)

    def test_final_answer_in_middle(self):
        msg = self._make_message("Here is the FINAL ANSWER for you.")
        self.assertEqual(get_next_node(msg, "next_node"), END)

    def test_partial_match_does_not_trigger(self):
        msg = self._make_message("This is the FINAL step but not an ANSWER.")
        self.assertEqual(get_next_node(msg, "next_node"), "next_node")

    def test_case_sensitive(self):
        msg = self._make_message("final answer in lowercase")
        self.assertEqual(get_next_node(msg, "next_node"), "next_node")

    def test_empty_content(self):
        msg = self._make_message("")
        self.assertEqual(get_next_node(msg, "fallback"), "fallback")


class TestShouldContinue(unittest.TestCase):
    """Tests for should_continue(state)"""

    def _make_state(self, tool_calls):
        last_msg = MagicMock()
        last_msg.tool_calls = tool_calls
        return {"messages": [MagicMock(), last_msg]}

    def test_returns_tool_node_when_tool_calls_present(self):
        state = self._make_state([{"name": "search", "args": {}}])
        self.assertEqual(should_continue(state), "tool_node")

    def test_returns_end_when_no_tool_calls(self):
        # Empty list is falsy → should return END
        state = self._make_state([])
        self.assertEqual(should_continue(state), END)

    def test_returns_end_when_tool_calls_none(self):
        state = self._make_state(None)
        self.assertEqual(should_continue(state), END)

    def test_uses_last_message_only(self):
        """Only the last message in the list should be inspected."""
        first_msg = MagicMock()
        first_msg.tool_calls = [{"name": "tool1"}]
        last_msg = MagicMock()
        last_msg.tool_calls = []
        state = {"messages": [first_msg, last_msg]}
        self.assertEqual(should_continue(state), END)

    def test_single_message_state(self):
        state = self._make_state([{"name": "calc"}])
        # Rebuild with single message
        msg = MagicMock()
        msg.tool_calls = [{"name": "calc"}]
        state = {"messages": [msg]}
        self.assertEqual(should_continue(state), "tool_node")


class TestMakeSystemPrompt(unittest.TestCase):
    """Tests for make_system_prompt(suffix)"""

    def test_contains_base_prompt(self):
        result = make_system_prompt("")
        self.assertIn("You are a helpful AI assistant", result)
        self.assertIn("FINAL ANSWER", result)

    def test_suffix_appended(self):
        suffix = "You specialize in Polish grammar."
        result = make_system_prompt(suffix)
        self.assertTrue(result.endswith(suffix))

    def test_empty_suffix(self):
        result = make_system_prompt("")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_suffix_with_newlines(self):
        suffix = "Line1\nLine2\nLine3"
        result = make_system_prompt(suffix)
        self.assertIn(suffix, result)

    def test_return_type_is_str(self):
        self.assertIsInstance(make_system_prompt("test"), str)


if __name__ == "__main__":
    unittest.main()
