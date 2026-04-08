from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command

from .utils import (
    story_teller_llm, make_system_prompt, compact_messages,
)

STORY_TELLER_PROMPT = (
    "Jesteś bajkopisarzem tworzącym historyjki edukacyjne po polsku.\n"
    "Na podstawie otrzymanego scenariusza zastosowania algorytmu, "
    "napisz krótką, angażującą historyjkę (3-5 akapitów).\n\n"
    "WAŻNE ZASADY:\n"
    "- Zamiast konkretnych imion bohaterów, używaj placeholderów: {IMIE_1}, {IMIE_2}, {IMIE_3} itd.\n"
    "- Zamiast konkretnych nazw miejsc, używaj placeholderów: {MIEJSCE_1}, {MIEJSCE_2} itd.\n"
    "- Historyjka musi naturalnie prowadzić do problemu, który rozwiązuje algorytm\n"
    "- Dane liczbowe w historyjce muszą być spójne z typami danych wejściowych algorytmu\n"
    "- Pisz w stylu prostym, ale wciągającym\n\n"
    "Gdy skończysz, poprzedź odpowiedź słowami FINAL ANSWER."
)

def story_teller(state: MessagesState) -> Command[Literal["text_checker"]]:
    """Creates a tale-style description of the task with placeholders for names and places."""

    agent = create_agent(
        model=story_teller_llm,
        tools=[],
        system_prompt=make_system_prompt(STORY_TELLER_PROMPT),
    )

    compact_state = {**state, "messages": compact_messages(state["messages"])}
    result = agent.invoke(compact_state)

    output_msg = HumanMessage(
        content=result["messages"][-1].content,
        name="story_teller",
    )

    return Command(
        update={
            "messages": [output_msg],
            "current_stage": "story_teller",
            "next_stage": "names_creator",
        },
        goto="text_checker",
    )

