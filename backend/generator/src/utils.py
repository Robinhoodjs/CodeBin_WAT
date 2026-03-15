import getpass
import os
from typing import Literal, Annotated

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage

from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState

load_dotenv()

analysis_llm = ChatOpenAI(
    model="gemma-3-4b",
    base_url=os.getenv("LMSTUDIO_ENDPOINT"),
    api_key=os.getenv("LMSTUDIO_API_KEY"),
    temperature=0.0,
)


story_teller_llm = ChatOpenAI(
    model="gemma-3-4b",
    base_url=os.getenv("LMSTUDIO_ENDPOINT"),
    api_key=os.getenv("LMSTUDIO_API_KEY"),
    temperature=0.7,
)

output_llm = ChatOpenAI(
    model="gemma-3-4b",
    base_url=os.getenv("LMSTUDIO_ENDPOINT"),
    api_key=os.getenv("LMSTUDIO_API_KEY"),
    temperature=0.3,
)

def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Wprowadź zmienną {var}: ")

_set_if_undefined("OPENAI_API_KEY")

from langchain_experimental.utilities import PythonREPL

repl = PythonREPL()


# ---------------------------------------------------------------------------
# Custom state – extends MessagesState with pipeline stage tracking
# ---------------------------------------------------------------------------
class AgentState(MessagesState):
    """Extended state that tracks which pipeline stage we are in."""
    current_stage: str   # e.g. "scenario_creator", "story_teller", ...
    next_stage: str      # where to go after successful validation


# ---------------------------------------------------------------------------
# Pipeline stage ordering
# ---------------------------------------------------------------------------
PIPELINE_STAGES = [
    "scenario_creator",
    "story_teller",
    "names_creator",
    "task_describer",
    "output_describer",
]

def get_next_pipeline_stage(current: str) -> str:
    """Return the next stage name or END."""
    try:
        idx = PIPELINE_STAGES.index(current)
        if idx + 1 < len(PIPELINE_STAGES):
            return PIPELINE_STAGES[idx + 1]
    except ValueError:
        pass
    return END


# ---------------------------------------------------------------------------
# Routing helpers
# ---------------------------------------------------------------------------
def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        return END
    return goto


def should_continue(state: MessagesState) -> Literal["tool_node", "__end__"]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tool_node"
    return END


def make_system_prompt(suffix: str) -> str:
    return (
        "You are a helpful AI assistant, collaborating with other assistants."
        " Use the provided tools to progress towards answering the question."
        " If you are unable to fully answer, that's OK, another assistant with different tools "
        " will help where you left off. Execute what you can to make progress."
        " If you or any of the other assistants have the final answer or deliverable,"
        " prefix your response with FINAL ANSWER so the team knows to stop."
        f"\n{suffix}"
    )


# ---------------------------------------------------------------------------
# Agent-specific system prompts
# ---------------------------------------------------------------------------

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