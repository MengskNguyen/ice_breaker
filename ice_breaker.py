from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile

information = """
Makima (マキマ?) is the main antagonist of the Public Safety Saga. She was the Chief Cabinet Secretary's Personal Devil Hunter who took Denji in as her human pet.

She is later revealed to be the Control Devil (支し配はいの悪あく魔ま Shihai no Akuma?) who embodies the fear of control or conquest and a member of the Four Horsemen at the time. Following her death, she was reincarnated as Nayuta.
"""


def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)

    summary_template = """"
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=['information'],
        template=summary_template
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")
    chain = summary_prompt_template | llm
    res = chain.invoke(input={'information': linkedin_data})
    print(res.content)


if __name__ == "__main__":
    print("Ice Breaker")
    load_dotenv()
    ice_break_with("Eden Marco")
