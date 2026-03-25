from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command

from .utils import (
    output_llm, make_system_prompt,
)

TASK_DESCRIBER_PROMPT = (
    "Jesteś nauczycielem programowania tworzącym treści zadań po polsku.\n"
    "Na podstawie otrzymanej historyjki i opisu algorytmu, "
    "wygeneruj zwięzłe i jasne WEZWANIE DO ROZWIĄZANIA ZADANIA.\n\n"
    "Wezwanie powinno:\n"
    "- Nawiązywać do historyjki (w 1-2 zdaniach)\n"
    "- Jasno opisywać, co program ma zrobić\n"
    "- Określić format danych wejściowych\n"
    "- Określić oczekiwany format danych wyjściowych\n"
    "- Podać przykład (wejście → wyjście)\n\n"
    "Pisz po polsku, w stylu profesjonalnym ale przystępnym.\n"
    "Gdy skończysz, poprzedź odpowiedź słowami FINAL ANSWER."
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
