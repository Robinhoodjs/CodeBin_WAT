from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command

from . import (
    story_teller_llm, make_system_prompt,
    SCENARIO_CREATOR_PROMPT, STORY_TELLER_PROMPT,
    NAMES_CREATOR_PROMPT, TASK_DESCRIBER_PROMPT, output_llm,
)


def scenario_creator(state: MessagesState) -> Command[Literal["text_checker"]]:
    """Generates a realistic usage scenario for the algorithm based on input analysis."""

    agent = create_agent(
        model=output_llm,
        tools=[],
        system_prompt=make_system_prompt(SCENARIO_CREATOR_PROMPT),
    )

    result = agent.invoke(state)

    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="scenario_creator",
    )

    return Command(
        update={
            "messages": result["messages"],
            "current_stage": "scenario_creator",
            "next_stage": "story_teller",
        },
        goto="text_checker",
    )


def story_teller(state: MessagesState) -> Command[Literal["text_checker"]]:
    """Creates a tale-style description of the task with placeholder names and places."""

    agent = create_agent(
        model=story_teller_llm,
        tools=[],
        system_prompt=make_system_prompt(STORY_TELLER_PROMPT),
    )

    result = agent.invoke(state)

    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="story_teller",
    )

    return Command(
        update={
            "messages": result["messages"],
            "current_stage": "story_teller",
            "next_stage": "names_creator",
        },
        goto="text_checker",
    )


def names_creator(state: MessagesState) -> Command[Literal["text_checker"]]:
    """Generates and inserts Polish names of persons and places into the tale."""

    agent = create_agent(
        model=story_teller_llm,
        tools=[],
        system_prompt=make_system_prompt(NAMES_CREATOR_PROMPT),
    )

    result = agent.invoke(state)

    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="names_creator",
    )

    return Command(
        update={
            "messages": result["messages"],
            "current_stage": "names_creator",
            "next_stage": "task_describer",
        },
        goto="text_checker",
    )


def task_describer(state: MessagesState) -> Command[Literal["text_checker"]]:
    """Generates a call-to-action for solving the programming task."""

    agent = create_agent(
        model=output_llm,
        tools=[],
        system_prompt=make_system_prompt(TASK_DESCRIBER_PROMPT),
    )

    result = agent.invoke(state)

    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="task_describer",
    )

    return Command(
        update={
            "messages": result["messages"],
            "current_stage": "task_describer",
            "next_stage": "output_describer",
        },
        goto="text_checker",
    )
