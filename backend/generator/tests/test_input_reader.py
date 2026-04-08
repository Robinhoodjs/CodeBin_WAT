import unittest
from unittest.mock import MagicMock, ANY
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
    os.path.join(os.path.dirname(__file__), os.pardir, "src", "agents/utils.py")
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
# Load input_reader.py source, strip relative imports, then exec
# ---------------------------------------------------------------------------
_ir_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "src", "agents/input_reader.py")
)

with open(_ir_path, "r", encoding="utf-8") as f:
    _ir_source = f.read()

_ir_source = re.sub(r'from \.utils import [^\n(]+\n', '\n', _ir_source)
_ir_source = re.sub(r'from \.\w+ import [^\n(]+\n', '\n', _ir_source)

_ir_mod = types.ModuleType("generator_input_reader")
_ir_mod.llm = MagicMock()
_ir_mod.analysis_llm = MagicMock()
_ir_mod.make_system_prompt = _utils_mod.make_system_prompt
_ir_mod.create_agent = MagicMock()
_ir_mod.HumanMessage = MagicMock()
_ir_mod.MessagesState = dict
_ir_mod.Command = MagicMock()
_ir_mod.Literal = None
_ir_mod.compact_messages = _utils_mod.compact_messages

exec(compile(_ir_source, _ir_path, "exec"), _ir_mod.__dict__)

input_reader = _ir_mod.input_reader


# ============================= TESTS ======================================


class TestInputReader(unittest.TestCase):
    """Tests for input_reader(state)"""

    def test_is_callable(self):
        self.assertTrue(callable(input_reader))

    def test_has_docstring(self):
        self.assertIsNotNone(input_reader.__doc__)
        self.assertIn("code", input_reader.__doc__.lower())

    def test_invokes_agent_with_state(self):
        """input_reader should create an agent and invoke it with the state."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: 2 inputs: int n, float x"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _ir_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": [MagicMock()]}
        input_reader(state)

        _ir_mod.create_agent.assert_called_once()
        mock_agent.invoke.assert_called_once()  # called with compact_state

    def test_returns_command_to_scenario_creator(self):
        """input_reader should route to scenario_creator."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: analysis"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _ir_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        input_reader(state)

        cmd_call = _ir_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "scenario_creator")

    def test_sets_current_and_next_stage(self):
        """input_reader should set current_stage and next_stage in Command update."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: analysis"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _ir_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        input_reader(state)

        cmd_call = _ir_mod.Command.call_args
        update = cmd_call.kwargs.get("update", cmd_call[1].get("update", {}))
        self.assertEqual(update["current_stage"], "input_reader")
        self.assertEqual(update["next_stage"], "scenario_creator")


if __name__ == "__main__":
    unittest.main()
