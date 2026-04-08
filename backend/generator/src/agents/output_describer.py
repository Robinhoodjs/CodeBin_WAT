from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, END
from langgraph.types import Command

from .utils import make_system_prompt, output_llm, compact_messages


OUTPUT_DESCRIBER_PROMPT = (
    "Jesteś ekspertem od dokumentacji technicznej po polsku.\n"
    "Na podstawie analizy kodu i wcześniejszych informacji, "
    "wygeneruj czytelny opis techniczny:\n\n"
    "1. DANE WEJŚCIOWE:\n"
    "   - Ile danych jest wczytywanych\n"
    "   - Jakiego są typu (int, float, string, ...)\n"
    "   - W jakim formacie są podawane\n\n"
    "2. DANE WYJŚCIOWE:\n"
    "   - Co zwraca / wypisuje program\n"
    "   - Jakiego typu jest wynik\n"
    "   - W jakim formacie jest prezentowany\n\n"
    "Pisz w formie listy punktowanej lub tabeli. "
    "Tekst ma być zrozumiały dla studenta programowania.\n"
    "Gdy skończysz, poprzedź odpowiedź słowami FINAL ANSWER."
)

def output_describer(state: MessagesState) -> Command[Literal["text_checker"]]:
    """Generates text describing how large input is, which types are demanded,
    and what output is returned by the code snippet."""

    agent = create_agent(
        model=output_llm,
        tools=[],
        system_prompt=make_system_prompt(OUTPUT_DESCRIBER_PROMPT),
    )

    compact_state = {**state, "messages": compact_messages(state["messages"])}
    result = agent.invoke(compact_state)

    output_msg = HumanMessage(
        content=result["messages"][-1].content,
        name="output_describer",
    )

    return Command(
        update={
            "messages": [output_msg],
            "current_stage": "output_describer",
            "next_stage": END,
        },
        goto="text_checker",
    )