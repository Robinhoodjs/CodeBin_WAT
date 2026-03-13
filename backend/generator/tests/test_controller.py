import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import types

# ---------------------------------------------------------------------------
# Mock heavy third-party dependencies before importing module under test
# ---------------------------------------------------------------------------
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("TAVILY_API_KEY", "test-key")

for mod_name in [
    "langchain_openai", "langchain_tavily", "langchain_experimental",
    "langchain_experimental.utilities", "dotenv", "langgraph",
    "langgraph.graph", "langgraph.types", "langchain_core",
    "langchain_core.messages", "langchain", "langchain.agents",
]:
    sys.modules.setdefault(mod_name, MagicMock())

sys.modules["langgraph.graph"].END = "__end__"
sys.modules["langgraph.graph"].MessagesState = dict

# ---------------------------------------------------------------------------
# Build utils functions (needed by controller)
# ---------------------------------------------------------------------------
import importlib.util

_utils_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "src", "utils.py")
)
_spec_u = importlib.util.spec_from_file_location("generator_utils", _utils_path)
_utils_mod = importlib.util.module_from_spec(_spec_u)
_utils_mod.END = "__end__"
_utils_mod.ChatOpenAI = MagicMock()
_utils_mod.load_dotenv = MagicMock()
_utils_mod.BaseMessage = MagicMock()
_utils_mod.MessagesState = dict
_utils_mod.TavilySearch = MagicMock()
_utils_mod.PythonREPL = MagicMock()
_utils_mod.getpass = MagicMock()
_utils_mod.os = os
_spec_u.loader.exec_module(_utils_mod)

# ---------------------------------------------------------------------------
# Load controller.py source, replace relative import, then exec
# ---------------------------------------------------------------------------
_ctrl_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "src", "controller.py")
)

with open(_ctrl_path, "r", encoding="utf-8") as f:
    _ctrl_source = f.read()

# Remove the relative import line — we inject deps manually
_ctrl_source = _ctrl_source.replace(
    "from . import llm, make_system_prompt, get_next_node", ""
)

_ctrl_mod = types.ModuleType("generator_controller")

# Inject everything the controller expects
_ctrl_mod.llm = MagicMock()
_ctrl_mod.make_system_prompt = _utils_mod.make_system_prompt
_ctrl_mod.get_next_node = _utils_mod.get_next_node
_ctrl_mod.create_agent = MagicMock()
_ctrl_mod.HumanMessage = MagicMock()
_ctrl_mod.MessagesState = dict
_ctrl_mod.Command = MagicMock()
_ctrl_mod.Literal = None
_ctrl_mod.END = "__end__"

# Provide the names that other top-level imports in controller.py expect
_ctrl_mod.__dict__["Literal"] = getattr(__builtins__, "None", None)

# Add all the imports the file does at the top
exec(compile(_ctrl_source, _ctrl_path, "exec"), _ctrl_mod.__dict__)

text_checker = _ctrl_mod.text_checker
text_corrector = _ctrl_mod.text_corrector
END = "__end__"


# ============================= TESTS ======================================


class TestTextChecker(unittest.TestCase):
    """Tests for text_checker(state)"""

    def test_invokes_agent_with_state(self):
        """text_checker should create an agent and invoke it with the state."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "Some corrected text"
        mock_agent.invoke.return_value = {"messages": [last_msg]}

        _ctrl_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": [MagicMock()]}
        text_checker(state)

        _ctrl_mod.create_agent.assert_called_once()
        mock_agent.invoke.assert_called_once_with(state)

    def test_calls_get_next_node_with_last_message(self):
        """text_checker should pass the last message to get_next_node."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: OK"
        mock_agent.invoke.return_value = {"messages": [last_msg]}

        _ctrl_mod.create_agent = MagicMock(return_value=mock_agent)

        with patch.object(_ctrl_mod, "get_next_node", wraps=_utils_mod.get_next_node) as mock_gnn:
            text_checker({"messages": []})
            mock_gnn.assert_called_once_with(last_msg, "text_corrector")

    def test_get_next_node_returns_end_on_final_answer(self):
        """When agent returns FINAL ANSWER, get_next_node should return END."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: Text is correct."
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _ctrl_mod.create_agent = MagicMock(return_value=mock_agent)

        result = _utils_mod.get_next_node(last_msg, "text_corrector")
        self.assertEqual(result, END)

    def test_get_next_node_returns_goto_without_final_answer(self):
        """When no FINAL ANSWER, get_next_node should return the goto node."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "There are errors to fix."
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _ctrl_mod.create_agent = MagicMock(return_value=mock_agent)

        result = _utils_mod.get_next_node(last_msg, "text_corrector")
        self.assertEqual(result, "text_corrector")


class TestTextCorrector(unittest.TestCase):
    """Tests for text_corrector()"""

    def test_is_callable(self):
        self.assertTrue(callable(text_corrector))

    def test_returns_none(self):
        """Current stub implementation returns None (pass)."""
        _ctrl_mod.create_agent = MagicMock()
        result = text_corrector()
        self.assertIsNone(result)

    def test_creates_agent_internally(self):
        """text_corrector should call create_agent."""
        mock_create = MagicMock()
        _ctrl_mod.create_agent = mock_create
        text_corrector()
        mock_create.assert_called_once()

    def test_accepts_no_arguments(self):
        """text_corrector should be callable with no args."""
        _ctrl_mod.create_agent = MagicMock()
        try:
            text_corrector()
        except TypeError:
            self.fail("text_corrector() raised TypeError unexpectedly")


if __name__ == "__main__":
    unittest.main()
