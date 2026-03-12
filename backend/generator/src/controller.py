
from langchain.agents import create_react_agent
from . import llm, make_system_prompt

text_checker_agent = create_react_agent(
    llm,
    tools = [],
    prompt=make_system_prompt(
        ""
    ),
)

def text_checker():
    """Checks semantic and syntactic correctness in Polish"""

    agent = create_react_agent(
        llm,
        tools=[],
        prompt=make_system_prompt(
            ""
        ),
    )
    pass


def text_corrector():
    """Introduces corrections into input text that were noticed"""
    pass
