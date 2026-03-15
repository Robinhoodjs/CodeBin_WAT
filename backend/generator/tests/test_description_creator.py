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
# Load description_creator.py source, strip relative imports, then exec
# ---------------------------------------------------------------------------
_dc_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "src", "description_creator.py")
)

with open(_dc_path, "r", encoding="utf-8") as f:
    _dc_source = f.read()

_dc_source = re.sub(r'from \. import \(.*?\)', '', _dc_source, flags=re.DOTALL)
_dc_source = re.sub(r'from \. import .+', '', _dc_source)

_dc_mod = types.ModuleType("generator_description_creator")
_dc_mod.llm = MagicMock()
_dc_mod.story_teller_llm = MagicMock()
_dc_mod.output_llm = MagicMock()
_dc_mod.make_system_prompt = _utils_mod.make_system_prompt
_dc_mod.SCENARIO_CREATOR_PROMPT = _utils_mod.SCENARIO_CREATOR_PROMPT
_dc_mod.STORY_TELLER_PROMPT = _utils_mod.STORY_TELLER_PROMPT
_dc_mod.NAMES_CREATOR_PROMPT = _utils_mod.NAMES_CREATOR_PROMPT
_dc_mod.TASK_DESCRIBER_PROMPT = _utils_mod.TASK_DESCRIBER_PROMPT
_dc_mod.create_agent = MagicMock()
_dc_mod.HumanMessage = MagicMock()
_dc_mod.MessagesState = dict
_dc_mod.Command = MagicMock()
_dc_mod.Literal = None

exec(compile(_dc_source, _dc_path, "exec"), _dc_mod.__dict__)

scenario_creator = _dc_mod.scenario_creator
story_teller = _dc_mod.story_teller
names_creator = _dc_mod.names_creator
task_describer = _dc_mod.task_describer


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
        _dc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": [MagicMock()]}
        scenario_creator(state)

        _dc_mod.create_agent.assert_called_once()
        mock_agent.invoke.assert_called_once_with(state)

    def test_routes_to_text_checker(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: scenario"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _dc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        scenario_creator(state)

        cmd_call = _dc_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "text_checker")

    def test_sets_stages(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: scenario"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _dc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        scenario_creator(state)

        cmd_call = _dc_mod.Command.call_args
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
        _dc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        story_teller(state)

        cmd_call = _dc_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "text_checker")

    def test_sets_next_stage_to_names_creator(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: story"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _dc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        story_teller(state)

        cmd_call = _dc_mod.Command.call_args
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
        _dc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        names_creator(state)

        cmd_call = _dc_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "text_checker")

    def test_sets_next_stage_to_task_describer(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: names"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _dc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        names_creator(state)

        cmd_call = _dc_mod.Command.call_args
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
        _dc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        task_describer(state)

        cmd_call = _dc_mod.Command.call_args
        self.assertEqual(cmd_call.kwargs.get("goto", cmd_call[1].get("goto", None)), "text_checker")

    def test_sets_next_stage_to_output_describer(self):
        mock_agent = MagicMock()
        last_msg = MagicMock()
        last_msg.content = "FINAL ANSWER: task"
        mock_agent.invoke.return_value = {"messages": [last_msg]}
        _dc_mod.create_agent = MagicMock(return_value=mock_agent)

        state = {"messages": []}
        task_describer(state)

        cmd_call = _dc_mod.Command.call_args
        update = cmd_call.kwargs.get("update", cmd_call[1].get("update", {}))
        self.assertEqual(update["next_stage"], "output_describer")


if __name__ == "__main__":
    unittest.main()
