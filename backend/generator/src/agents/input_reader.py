from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command

from .utils import make_system_prompt, analysis_llm, compact_messages

INPUT_READER_PROMPT = (
    "Jesteś ekspertem od analizy kodu źródłowego.\n"
    "Twoim zadaniem jest przeanalizowanie podanego fragmentu kodu i określenie:\n"
    "1. Ile danych wejściowych przyjmuje kod (liczba zmiennych/argumentów wczytywanych)\n"
    "2. Jakiego typu są te dane (int, float, string, bool, lista, tablica, itp.)\n"
    "3. W jakim formacie są wczytywane (np. jedna linia, wiele linii, separowane spacjami)\n"
    "4. Jaki jest zakres/ograniczenia wartości (jeśli wynikają z kodu)\n\n"
    "Odpowiedz w formie strukturalnej, np.:\n"
    "- Liczba danych wejściowych: N\n"
    "- Dane: typ1 nazwa1, typ2 nazwa2, ...\n"
    "- Format wczytywania: opis\n\n"
    "Odpowiadaj ZAWSZE po polsku.\n"
    "Gdy skończysz analizę, poprzedź swoją odpowiedź słowami FINAL ANSWER."
)


def input_reader(state: MessagesState) -> Command[Literal["scenario_creator"]]:
    """Inspects code and returns format information: how many values, what primitive types
    (int, float, bool, string, ...) and in what format the code reads its input."""

    agent = create_agent(
        model=analysis_llm,
        tools=[],
        system_prompt=make_system_prompt(INPUT_READER_PROMPT),
    )

    compact_state = {**state, "messages": compact_messages(state["messages"])}
    result = agent.invoke(compact_state)

    output_msg = HumanMessage(
        content=result["messages"][-1].content,
        name="input_reader",
    )

    return Command(
        update={
            "messages": [output_msg],
            "current_stage": "input_reader",
            "next_stage": "scenario_creator",
        },
        goto="scenario_creator",
    )
