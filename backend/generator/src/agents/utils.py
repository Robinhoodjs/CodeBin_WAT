import getpass
import os
from typing import Literal

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import END, MessagesState

ENDPOINT = os.getenv("LMSTUDIO_ENDPOINT")
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "google/gemma-3-4b"

analysis_llm = ChatOpenAI(
    model=MODEL,
    base_url=ENDPOINT,
    api_key=API_KEY,
    temperature=0.0,
)


story_teller_llm = ChatOpenAI(
    model=MODEL,
    base_url=ENDPOINT,
    api_key=API_KEY,
    temperature=0.7,
)

output_llm = ChatOpenAI(
    model=MODEL,
    base_url=ENDPOINT,
    api_key=API_KEY,
    temperature=0.3,
)

def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Wprowadź zmienną {var}: ")

_set_if_undefined("OPENAI_API_KEY")

from langchain_experimental.utilities import PythonREPL

repl = PythonREPL()


class AgentState(MessagesState):
    """Extended state that tracks which pipeline stage we are in."""
    current_stage: str   # e.g. "scenario_creator", "story_teller", ...
    next_stage: str      # where to go after successful validation


PIPELINE_STAGES = [
    "scenario_creator",
    "story_teller",
    "names_creator",
    "task_describer",
    "output_describer",
]

def get_next_pipeline_stage(current: str) -> str:
    """Return the next stage name or END."""
    try:
        idx = PIPELINE_STAGES.index(current)
        if idx + 1 < len(PIPELINE_STAGES):
            return PIPELINE_STAGES[idx + 1]
    except ValueError:
        pass
    return END


# ---------------------------------------------------------------------------
# Routing helpers
# ---------------------------------------------------------------------------
def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        return END
    return goto


def should_continue(state: MessagesState) -> Literal["tool_node", "__end__"]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tool_node"
    return END


def make_system_prompt(suffix: str) -> str:
    return (
        "You are a helpful AI assistant, collaborating with other assistants."
        " Use the provided tools to progress towards answering the question."
        " If you are unable to fully answer, that's OK, another assistant with different tools "
        " will help where you left off. Execute what you can to make progress."
        " If you or any of the other assistants have the final answer or deliverable,"
        " prefix your response with FINAL ANSWER so the team knows to stop."
        f"\n{suffix}"
    )

