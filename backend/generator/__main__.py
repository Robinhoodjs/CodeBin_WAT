from dotenv import load_dotenv
from langgraph.graph import StateGraph, START

load_dotenv()

from backend.generator.src.agents import (
    AgentState,
    input_reader,
    scenario_creator,
    story_teller,
    names_creator,
    task_describer,
    output_describer,
    text_checker,
    text_corrector
)

# ---------------------------------------------------------------------------
# Build the LangGraph workflow
# ---------------------------------------------------------------------------
workflow = StateGraph(AgentState)

# Register all nodes
workflow.add_node("input_reader", input_reader)
workflow.add_node("scenario_creator", scenario_creator)
workflow.add_node("story_teller", story_teller)
workflow.add_node("names_creator", names_creator)
workflow.add_node("task_describer", task_describer)
workflow.add_node("output_describer", output_describer)
workflow.add_node("text_checker", text_checker)
workflow.add_node("text_corrector", text_corrector)

# ---------------------------------------------------------------------------
# Edges — linear pipeline with validation loops
# ---------------------------------------------------------------------------
# START → input_reader → scenario_creator
workflow.add_edge(START, "input_reader")
workflow.add_edge("input_reader", "scenario_creator")
# workflow.add_edge("scenario_creator", "story_teller")
# workflow.add_edge("story_teller", "names_creator")
# workflow.add_edge("names_creator", "task_describer")
# workflow.add_edge("task_describer", "output_describer")
# workflow.add_edge("output_describer", "text_checker")
# workflow.add_conditional_edges(
#     "text_checker",
#     should_continue,
#     ["text_corrector", END],
# )

graph = workflow.compile()


def visualize():
    """Render the graph as a Mermaid PNG (requires IPython)."""
    from IPython.display import Image, display
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        pass

def run(code: str):
    """Execute the full pipeline on a given code snippet.

    Args:
        code: Source code to generate a task description for.

    Returns:
        List of messages produced by the pipeline.
    """
    from langchain_core.messages import HumanMessage
    messages = [
        HumanMessage(
            content=f"Przeanalizuj poniższy kod i wygeneruj zadanie programistyczne:\n\n```\n{code}\n```"
        )
    ]

    result = graph.invoke({
        "messages": messages,
        "current_stage": "",
        "next_stage": "scenario_creator",
    })

    return result["messages"]


if __name__ == "__main__":
    import sys
    import os

    # Try to read code from resources/code.txt or from command-line argument
    code_path = os.path.join(os.path.dirname(__file__), os.pardir, "generator/resources", "code.txt")

    if len(sys.argv) > 1:
        code = sys.argv[1]
    elif os.path.exists(code_path):
        with open(code_path, "r", encoding="utf-8") as f:
            code = f.read().strip()
    else:
        code = input("Podaj kod do analizy:\n")

    if not code:
        print("Brak kodu do analizy. Podaj kod jako argument lub wpisz do resources/code.txt")
        sys.exit(1)

    messages = run(code)

    print("\n" + "=" * 60)
    print("WYNIKI PIPELINE")
    print("=" * 60)
    for m in messages:
        m.pretty_print()