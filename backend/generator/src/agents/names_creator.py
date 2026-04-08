from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command

from .utils import (
    story_teller_llm, make_system_prompt, compact_messages,
)

NAMES_CREATOR_PROMPT = (
    "Jesteś asystentem do generowania imion i nazw po polsku.\n"
    "Otrzymasz historyjkę z placeholderami {IMIE_1}, {IMIE_2}, ..., {MIEJSCE_1}, {MIEJSCE_2}, ...\n\n"
    "Twoim zadaniem jest:\n"
    "1. Wybrać polskie imiona dla każdego placeholdera {IMIE_X} (np. Anna, Tomek, Kasia)\n"
    "2. Wybrać polskie nazwy miejsc dla każdego placeholdera {MIEJSCE_X} (np. Kraków, Warszawa, Leśna Polana)\n"
    "3. Podstawić wybrane imiona i nazwy w treści historyjki\n"
    "4. Zwrócić pełny tekst historyjki z wypełnionymi placeholderami\n\n"
    "Imiona i miejsca powinny pasować do kontekstu historyjki.\n"
    "Gdy skończysz, poprzedź odpowiedź słowami FINAL ANSWER."
)


def names_creator(state: MessagesState) -> Command[Literal["text_checker"]]:
    """Generates and inserts Polish names of persons and places into the tale."""

    agent = create_agent(
        model=story_teller_llm,
        tools=[],
        system_prompt=make_system_prompt(NAMES_CREATOR_PROMPT),
    )

    compact_state = {**state, "messages": compact_messages(state["messages"])}
    result = agent.invoke(compact_state)

    output_msg = HumanMessage(
        content=result["messages"][-1].content,
        name="names_creator",
    )

    return Command(
        update={
            "messages": [output_msg],
            "current_stage": "names_creator",
            "next_stage": "task_describer",
        },
        goto="text_checker",
    )

