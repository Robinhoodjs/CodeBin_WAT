import getpass
import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage

from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState

llm = ChatOpenAI(model="gpt-5.2")
load_dotenv()

def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Wprowadź zmienną {var}: ")

_set_if_undefined("OPENAI_API_KEY")
_set_if_undefined("TAVILY_API_KEY")

from langchain_tavily import TavilySearch
from langchain_experimental.utilities import PythonREPL

tavily_tool = TavilySearch(max_results = 5)
repl = PythonREPL()

def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        return END
    return goto

def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tool_node"
    return END