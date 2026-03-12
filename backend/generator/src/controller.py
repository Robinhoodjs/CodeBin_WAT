from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command

from . import llm, make_system_prompt, get_next_node

text_checker_agent = create_agent(
    model=llm,
    tools = [],
    system_prompt=make_system_prompt(
        ""
    ),
)

def text_checker(state: MessagesState) -> Command[Literal["text_corrector", "END"]]:
    """Checks semantic and syntactic correctness in Polish"""

    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=make_system_prompt(
            ""
        ),
    )
    result = agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "text_corrector")

    # result["messages"][-1] = HumanMessage(
    #     content=result["messages"][-1].content,
    #     name="researcher"
    # )
    # return Command(
    #     update={
    #         "messages": result["messages"],
    #     },
    #     goto=goto,
    # )


def text_corrector():
    """Introduces corrections into input text that were noticed"""
    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=make_system_prompt(
            ""
        ),
    )

    pass
