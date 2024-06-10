import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)

load_dotenv()


def lookup(name: str) -> str:
    return "abc"
