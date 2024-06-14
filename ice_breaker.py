from typing import Tuple

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)

    summary_template = """"
        given the information {information}, and twitter posts {twitter_posts} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        
        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=['information', 'twitter_posts'],
        template=summary_template,
        partial_variables={'format_instructions': summary_parser.get_format_instructions()}
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")
    chain = summary_prompt_template | llm | summary_parser
    res: Summary = chain.invoke(input={'information': linkedin_data, 'twitter_posts': tweets})
    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Ice Breaker")
    load_dotenv()
    ice_break_with("Eden Marco")
