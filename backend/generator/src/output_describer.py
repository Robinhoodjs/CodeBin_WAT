from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, END
from langgraph.types import Command

from . import output_llm, make_system_prompt, OUTPUT_DESCRIBER_PROMPT


def output_describer(state: MessagesState) -> Command[Literal["text_checker"]]:
    """Generates text describing how large input is, which types are demanded,
    and what output is returned by the code snippet."""

    agent = create_agent(
        model=output_llm,
        tools=[],
        system_prompt=make_system_prompt(OUTPUT_DESCRIBER_PROMPT),
    )

    result = agent.invoke(state)

    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="output_describer",
    )

    return Command(
        update={
            "messages": result["messages"],
            "current_stage": "output_describer",
            "next_stage": END,
        },
        goto="text_checker",
    )