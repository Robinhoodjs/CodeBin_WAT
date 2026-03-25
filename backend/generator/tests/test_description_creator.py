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
# Helper: load an agent source file, strip relative imports, exec into module
# ---------------------------------------------------------------------------
def _load_agent_module(filename, mod_name, extra_attrs=None):
    """Load an agent file by stripping relative imports and exec'ing."""
    _path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, "src", f"agents/{filename}")
    )
    with open(_path, "r", encoding="utf-8") as f:
        _source = f.read()
    _source = re.sub(r'from \.utils import \(.*?\)', '', _source, flags=re.DOTALL)
    _source = re.sub(r'from \.\w+ import [^\n(]+\n', '\n', _source)

    _mod = types.ModuleType(mod_name)
    _mod.llm = MagicMock()
    _mod.story_teller_llm = MagicMock()
    _mod.output_llm = MagicMock()
    _mod.make_system_prompt = _utils_mod.make_system_prompt
    _mod.create_agent = MagicMock()
    _mod.HumanMessage = MagicMock()
    _mod.MessagesState = dict
    _mod.Command = MagicMock()
    _mod.Literal = None
    _mod.END = "__end__"
    if extra_attrs:
        for k, v in extra_attrs.items():
            setattr(_mod, k, v)

    exec(compile(_source, _path, "exec"), _mod.__dict__)
    return _mod

_sc_mod = _load_agent_module("scenario_creator.py", "gen_scenario_creator")
_st_mod = _load_agent_module("story_teller.py", "gen_story_teller")
_nc_mod = _load_agent_module("names_creator.py", "gen_names_creator")
_td_mod = _load_agent_module("task_describer.py", "gen_task_describer")

scenario_creator = _sc_mod.scenario_creator
story_teller = _st_mod.story_teller
names_creator = _nc_mod.names_creator
task_describer = _td_mod.task_describer


# ============================= TESTS ======================================


class TestScenarioCreator(unittest.TestCase):
    """Tests for scenario_creator(state)"""

    def test_is_callable(self):
        self.assertTrue(callable(scenario_creator))

    def test_has_docstring(self):
        self.assertIsNotNone(scenario_creator.__doc__)

    def test_invokes_agent_with_state(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: scenario"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _sc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": [MagicMock()]}
        scenario_creator(state)

        _sc_mod.create_agent.assert_called_once()
        mock_agent.invoke.assert_called_once_with(state)

    def test_routes_to_text_checker(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: scenario"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _sc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        scenario_creator(state)

        cmd_call = _sc_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "text_checker")

    def test_sets_stages(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: scenario"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _sc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        scenario_creator(state)

        cmd_call = _sc_mod.Command.call_args
        update = cmd_call.kwargs.get("update", cmd_call[1].get("update", {}))
        self.assertEqual(update["current_stage"], "scenario_creator")
        self.assertEqual(update["next_stage"], "story_teller")


class TestStoryTeller(unittest.TestCase):
    """Tests for story_teller(state)"""

    def test_is_callable(self):
        self.assertTrue(callable(story_teller))

    def test_has_docstring(self):
        self.assertIsNotNone(story_teller.__doc__)
        self.assertIn("tale", story_teller.__doc__.lower())

    def test_invokes_agent_and_routes_to_text_checker(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: {IMIE_1} went to {MIEJSCE_1}"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _st_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        story_teller(state)

        cmd_call = _st_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "text_checker")

    def test_sets_next_stage_to_names_creator(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: story"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _st_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        story_teller(state)

        cmd_call = _st_mod.Command.call_args
        update = cmd_call.kwargs.get("update", cmd_call[1].get("update", {}))
        self.assertEqual(update["next_stage"], "names_creator")


class TestNamesCreator(unittest.TestCase):
    """Tests for names_creator(state)"""

    def test_is_callable(self):
        self.assertTrue(callable(names_creator))

    def test_has_docstring(self):
        self.assertIsNotNone(names_creator.__doc__)
        self.assertIn("names", names_creator.__doc__.lower())

    def test_invokes_agent_and_routes_to_text_checker(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: Anna went to Kraków"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _nc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        names_creator(state)

        cmd_call = _nc_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "text_checker")

    def test_sets_next_stage_to_task_describer(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: names"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _nc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        names_creator(state)

        cmd_call = _nc_mod.Command.call_args
        update = cmd_call.kwargs.get("update", cmd_call[1].get("update", {}))
        self.assertEqual(update["next_stage"], "task_describer")


class TestTaskDescriber(unittest.TestCase):
    """Tests for task_describer(state)"""

    def test_is_callable(self):
        self.assertTrue(callable(task_describer))

    def test_has_docstring(self):
        self.assertIsNotNone(task_describer.__doc__)
        self.assertIn("task", task_describer.__doc__.lower())

    def test_invokes_agent_and_routes_to_text_checker(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: Rozwiąż zadanie"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _td_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        task_describer(state)

        cmd_call = _td_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "text_checker")

    def test_sets_next_stage_to_output_describer(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: task"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _td_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        task_describer(state)

        cmd_call = _td_mod.Command.call_args
        update = cmd_call.kwargs.get("update", cmd_call[1].get("update", {}))
        self.assertEqual(update["next_stage"], "output_describer")


if __name__ == "__main__":
    unittest.main()
