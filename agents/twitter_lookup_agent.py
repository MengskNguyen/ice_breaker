import os
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)

from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name='gpt-4'
    )

    template = """
        given the full name {name_of_person} I want you to get me a link to their Twitter profile page.
        Your response should contain only a person's username
    """

    prompt_template = PromptTemplate(
        template=template,
        input_variables=['name_of_person']
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for Twitter profile username",
            func=get_profile_url_tavily,
            description="userful for when you need to get the Twitter profile username"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result['output']
    return linkedin_profile_url


if __name__ == "__main__":
    linkedin_url = lookup(name='Eden Marco')
    print(linkedin_url)
