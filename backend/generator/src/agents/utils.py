import getpass
import os
from typing import Literal

from langchain_core.messages import BaseMessage, HumanMessage
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
    max_tokens=2048

)


story_teller_llm = ChatOpenAI(
    model=MODEL,
    base_url=ENDPOINT,
    api_key=API_KEY,
    temperature=0.7,
    max_tokens=2048
)

output_llm = ChatOpenAI(
    model=MODEL,
    base_url=ENDPOINT,
    api_key=API_KEY,
    temperature=0.3,
    max_tokens=2048
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
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tool_node"
    return END


def make_system_prompt(suffix: str) -> str:
    return (
        "Jesteś asystentem AI współpracującym z innymi asystentami."
        " Wykonaj swoje zadanie najlepiej jak potrafisz."
        " Gdy skończysz, poprzedź odpowiedź słowami FINAL ANSWER."
        f"\n{suffix}"
    )



def compact_messages(messages, max_last_chars=1500):
    """Aggressively compact message history to prevent context overflow.

    Only keeps the LAST message (truncated if needed).
    Each agent only needs the previous stage's output to do its work.

    Args:
        messages: Full list of messages from the pipeline state.
        max_last_chars: Max characters to keep from the last message.

    Returns:
        List with at most 1 message.
    """
    if not messages:
        return []

    last = messages[-1]
    content = getattr(last, 'content', '') or ''

    # Truncate if too long
    if len(content) > max_last_chars:
        content = content[:max_last_chars] + "\n…[skrócono]"

    return [HumanMessage(content=content, name=getattr(last, 'name', None))]
