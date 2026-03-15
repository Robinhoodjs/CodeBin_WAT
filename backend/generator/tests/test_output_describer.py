import unittest
from unittest.mock import MagicMock
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
# Load output_describer.py source, strip relative imports, then exec
# ---------------------------------------------------------------------------
_od_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "src", "output_describer.py")
)

with open(_od_path, "r", encoding="utf-8") as f:
    _od_source = f.read()

_od_source = re.sub(r'from \. import \(.*?\)', '', _od_source, flags=re.DOTALL)
_od_source = re.sub(r'from \. import .+', '', _od_source)

_od_mod = types.ModuleType("generator_output_describer")
_od_mod.llm = MagicMock()
_od_mod.output_llm = MagicMock()
_od_mod.make_system_prompt = _utils_mod.make_system_prompt
_od_mod.OUTPUT_DESCRIBER_PROMPT = _utils_mod.OUTPUT_DESCRIBER_PROMPT
_od_mod.create_agent = MagicMock()
_od_mod.HumanMessage = MagicMock()
_od_mod.MessagesState = dict
_od_mod.Command = MagicMock()
_od_mod.END = "__end__"
_od_mod.Literal = None

exec(compile(_od_source, _od_path, "exec"), _od_mod.__dict__)

output_describer = _od_mod.output_describer
END = "__end__"


# ============================= TESTS ======================================


class TestOutputDescriber(unittest.TestCase):
    """Tests for output_describer(state)"""

    def test_is_callable(self):
        self.assertTrue(callable(output_describer))

    def test_has_docstring(self):
        self.assertIsNotNone(output_describer.__doc__)

    def test_invokes_agent_with_state(self):
        """output_describer should create an agent and invoke it with the state."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: Input: 2 int, Output: 1 int"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _od_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": [MagicMock()]}
        output_describer(state)

        _od_mod.create_agent.assert_called_once()
        mock_agent.invoke.assert_called_once_with(state)

    def test_routes_to_text_checker(self):
        """output_describer should route to text_checker."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: description"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _od_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        output_describer(state)

        cmd_call = _od_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "text_checker")

    def test_sets_next_stage_to_end(self):
        """output_describer is the last stage — next_stage should be END."""
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: description"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _od_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        output_describer(state)

        cmd_call = _od_mod.Command.call_args
        update = cmd_call.kwargs.get("update", cmd_call[1].get("update", {}))
        self.assertEqual(update["next_stage"], END)


if __name__ == "__main__":
    unittest.main()
