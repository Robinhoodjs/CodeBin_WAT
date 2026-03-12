from langgraph.graph import StateGraph, START
from langgraph.graph import MessagesState, END
from . import should_continue, input_reader, output_describer, text_checker, text_corrector, story_teller, names_creator, task_describer

workflow = StateGraph(MessagesState)
workflow.add_node("input_reader", input_reader)
workflow.add_node("scenario_creator", )
workflow.add_node("story_teller", )
workflow.add_node("names_creator", )
workflow.add_node("task_describer", )
workflow.add_node("text_checker", )
workflow.add_node("text_corrector", )
workflow.add_node("output_describer", )

workflow.add_edge(START, "input_reader")
workflow.add_edge("input_reader", "scenario_creator")
workflow.add_conditional_edges(
    "text_checker",
    should_continue,
    ["text_corrector", END],
)

workflow.add_edge("output_describer", END)
graph = workflow.compile()

from IPython.display import Image, display
try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    pass


from langchain.messages import HumanMessage
messages = [
    HumanMessage(
        content=
        """
        CODE
        """
    )
]
messages = graph.invoke({"messages": messages})

for m in messages["messages"]:
    m.pretty_print()