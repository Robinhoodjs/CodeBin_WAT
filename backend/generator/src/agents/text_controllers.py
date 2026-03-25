from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import END
from langgraph.types import Command

from .utils import (
    make_system_prompt,
    AgentState, analysis_llm, output_llm,
)



TEXT_CHECKER_PROMPT = (
    "Jesteś korektorem tekstów w języku polskim.\n"
    "Twoim zadaniem jest sprawdzenie otrzymanego tekstu pod kątem:\n"
    "1. Poprawności gramatycznej i ortograficznej\n"
    "2. Poprawności interpunkcyjnej\n"
    "3. Spójności semantycznej (czy tekst ma sens, jest logiczny)\n"
    "4. Naturalności stylu (czy brzmi naturalnie po polsku)\n\n"
    "Jeśli tekst jest POPRAWNY — odpowiedz:\n"
    "FINAL ANSWER: Tekst jest poprawny.\n"
    "[tutaj pełny oryginalny tekst bez zmian]\n\n"
    "Jeśli tekst ZAWIERA BŁĘDY — wymień je w postaci listy:\n"
    "BŁĘDY:\n"
    "- opis błędu 1\n"
    "- opis błędu 2\n"
    "...\n"
    "Następnie podaj poprawioną wersję tekstu.\n"
 
    "NIE używaj słów FINAL ANSWER jeśli są błędy."
)

def text_checker(state: AgentState) -> Command[Literal["text_corrector", "__end__"]]:
    """Checks semantic and syntactic correctness in Polish.

    If text is correct → routes to next_stage (via FINAL ANSWER).
    If text has errors → routes to text_corrector.
    """

    agent = create_agent(
        model=analysis_llm,
        tools=[],
        system_prompt=make_system_prompt(TEXT_CHECKER_PROMPT),
    )

    result = agent.invoke(state)
    last_message = result["messages"][-1]

    # Determine routing: FINAL ANSWER → next pipeline stage, otherwise → corrector
    if "FINAL ANSWER" in last_message.content:
        next_stage = state.get("next_stage", END)
        goto = next_stage
    else:
        goto = "text_corrector"

    result["messages"][-1] = HumanMessage(
        content=last_message.content,
        name="text_checker",
    )

    return Command(
        update={
            "messages": result["messages"],
        },
        goto=goto,
    )


TEXT_CORRECTOR_PROMPT = (
    "Jesteś ekspertem od korekty tekstów po polsku.\n"
    "Otrzymasz tekst wraz z listą błędów znalezionych przez korektora.\n\n"
    "Twoim zadaniem jest:\n"
    "1. Przeczytać oryginalny tekst i listę błędów\n"
    "2. Poprawić WSZYSTKIE wymienione błędy\n"
    "3. Zachować oryginalny styl i intencję tekstu\n"
    "4. Zwrócić poprawioną wersję tekstu\n\n"
    "Gdy skończysz, poprzedź odpowiedź słowami FINAL ANSWER, "
    "a następnie podaj pełny poprawiony tekst."
)

def text_corrector(state: AgentState) -> Command[Literal["text_checker"]]:
    """Introduces corrections into text based on errors found by text_checker.

    Always routes back to text_checker for re-validation.
    """

    agent = create_agent(
        model=output_llm,
        tools=[],
        system_prompt=make_system_prompt(TEXT_CORRECTOR_PROMPT),
    )

    result = agent.invoke(state)

    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="text_corrector",
    )

    return Command(
        update={
            "messages": result["messages"],
        },
        goto="text_checker",
    )
