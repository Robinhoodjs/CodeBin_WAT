import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import re
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
# Build utils module
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
_utils_mod.PythonREPL = MagicMock()
_utils_mod.getpass = MagicMock()
_utils_mod.os = os
_spec_u.loader.exec_module(_utils_mod)

# ---------------------------------------------------------------------------
# Load controller.py source, strip relative imports, then exec
# ---------------------------------------------------------------------------
_ctrl_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "src", "controller.py")
)

with open(_ctrl_path, "r", encoding="utf-8") as f:
    _ctrl_source = f.read()

# Strip all relative imports (single-line and multi-line)
_ctrl_source = re.sub(r'from \. import \([^)]*\)', '', _ctrl_source, flags=re.DOTALL)
_ctrl_source = re.sub(r'from \. import [^\n(]+\n', '\n', _ctrl_source)

_ctrl_mod = types.ModuleType("generator_controller")

# Inject everything the controller expects
_ctrl_mod.llm = MagicMock()
_ctrl_mod.analysis_llm = MagicMock()
_ctrl_mod.output_llm = MagicMock()
_ctrl_mod.make_system_prompt = _utils_mod.make_system_prompt
_ctrl_mod.get_next_node = _utils_mod.get_next_node
_ctrl_mod.create_agent = MagicMock()
_ctrl_mod.HumanMessage = MagicMock()
_ctrl_mod.MessagesState = dict
_ctrl_mod.Command = MagicMock()
_ctrl_mod.Literal = None
_ctrl_mod.END = "__end__"
_ctrl_mod.TEXT_CHECKER_PROMPT = _utils_mod.TEXT_CHECKER_PROMPT
_ctrl_mod.TEXT_CORRECTOR_PROMPT = _utils_mod.TEXT_CORRECTOR_PROMPT
_ctrl_mod.AgentState = _utils_mod.AgentState

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

        state = {"messages": [MagicMock()], "current_stage": "scenario_creator", "next_stage": "story_teller"}
        text_checker(state)

        _ctrl_mod.create_agent.assert_called_once()
        mock_agent.invoke.assert_called_once_with(state)

    def test_routes_to_text_corrector_when_errors(self):
        """text_checker should route to text_corrector when no FINAL ANSWER."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "BŁĘDY:\n- literówka w słowie"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _ctrl_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": [], "current_stage": "scenario_creator", "next_stage": "story_teller"}
        text_checker(state)

        cmd_call = _ctrl_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "text_corrector")

    def test_routes_to_next_stage_on_final_answer(self):
        """text_checker should route to next_stage on FINAL ANSWER."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: Tekst jest poprawny."
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _ctrl_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": [], "current_stage": "scenario_creator", "next_stage": "story_teller"}
        text_checker(state)

        cmd_call = _ctrl_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "story_teller")

    def test_is_callable(self):
        self.assertTrue(callable(text_checker))

    def test_has_docstring(self):
        self.assertIsNotNone(text_checker.__doc__)


class TestTextCorrector(unittest.TestCase):
    """Tests for text_corrector()"""

    def test_is_callable(self):
        self.assertTrue(callable(text_corrector))

    def test_invokes_agent_and_returns_command(self):
        """text_corrector should create an agent, invoke it, and return a Command."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: Poprawiony tekst."
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _ctrl_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": [MagicMock()], "current_stage": "story_teller", "next_stage": "names_creator"}
        text_corrector(state)

        _ctrl_mod.create_agent.assert_called_once()
        mock_agent.invoke.assert_called_once_with(state)

    def test_routes_to_text_checker(self):
        """text_corrector should always route back to text_checker."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: Poprawiony tekst."
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _ctrl_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": [], "current_stage": "story_teller", "next_stage": "names_creator"}
        text_corrector(state)

        cmd_call = _ctrl_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "text_checker")

    def test_has_docstring(self):
        self.assertIsNotNone(text_corrector.__doc__)


if __name__ == "__main__":
    unittest.main()
