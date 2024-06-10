from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile

information = """
Makima (マキマ?) is the main antagonist of the Public Safety Saga. She was the Chief Cabinet Secretary's Personal Devil Hunter who took Denji in as her human pet.

She is later revealed to be the Control Devil (支し配はいの悪あく魔ま Shihai no Akuma?) who embodies the fear of control or conquest and a member of the Four Horsemen at the time. Following her death, she was reincarnated as Nayuta.
"""

if __name__ == "__main__":
    print("Hello Langchain")
    load_dotenv()
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

    # chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    chain = summary_prompt_template | llm
    linkedin_data = scrape_linkedin_profile(
            linkedin_profile_url='https://www.linkedin.com/in/eden-marco',
            mock=True
        )
    res = chain.invoke(input={'information': linkedin_data})
    print(res.content)
