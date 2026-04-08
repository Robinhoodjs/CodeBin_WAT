from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command

from .utils import output_llm, make_system_prompt, compact_messages

SCENARIO_CREATOR_PROMPT = (
    "Jesteś kreatywnym pisarzem scenariuszy edukacyjnych.\n"
    "Na podstawie otrzymanej analizy kodu (typy danych wejściowych, opis algorytmu) "
    "wygeneruj realistyczny, ciekawy scenariusz zastosowania tego algorytmu w życiu codziennym.\n\n"
    "Scenariusz powinien:\n"
    "- Opisywać konkretną sytuację, w której algorytm jest przydatny\n"
    "- Być zrozumiały dla studenta informatyki\n"
    "- Zawierać kontekst, który naturalnie prowadzi do użycia tego algorytmu\n"
    "- Być napisany po polsku\n\n"
    "Gdy skończysz, poprzedź odpowiedź słowami FINAL ANSWER."
)

def scenario_creator(state: MessagesState) -> Command[Literal["text_checker"]]:
    """Generates a realistic usage scenario for the algorithm based on input analysis."""

    agent = create_agent(
        model=output_llm,
        tools=[],
        system_prompt=make_system_prompt(SCENARIO_CREATOR_PROMPT),
    )

    compact_state = {**state, "messages": compact_messages(state["messages"])}
    result = agent.invoke(compact_state)

    output_msg = HumanMessage(
        content=result["messages"][-1].content,
        name="scenario_creator",
    )

    return Command(
        update={
            "messages": [output_msg],
            "current_stage": "scenario_creator",
            "next_stage": "story_teller",
        },
        goto="text_checker",
    )
