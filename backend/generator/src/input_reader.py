from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command

from . import make_system_prompt, get_next_node, INPUT_READER_PROMPT, analysis_llm


def input_reader(state: MessagesState) -> Command[Literal["scenario_creator"]]:
    """Inspects code and returns format information: how many values, what primitive types
    (int, float, bool, string, ...) and in what format the code reads its input."""

    agent = create_agent(
        model=analysis_llm,
        tools=[],
        system_prompt=make_system_prompt(INPUT_READER_PROMPT),
    )

    result = agent.invoke(state)

    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="input_reader",
    )

    return Command(
        update={
            "messages": result["messages"],
            "current_stage": "input_reader",
            "next_stage": "scenario_creator",
        },
        goto="scenario_creator",
    )
