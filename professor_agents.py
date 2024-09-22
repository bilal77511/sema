from crewai import Agent
from langchain_openai import ChatOpenAI
from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
import os

class ProfessorAgents():
 
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL"),
            base_url=os.getenv("API_ENDPOINT"),
            api_key=os.getenv("API_KEY")
        )

    def university_finder_agent(self):
        return Agent(
            role='Public Research University Finder',
            goal='Find all public research universities in a given city or state',
            backstory='An expert in higher education institutions with a focus on public research universities',
            tools=[
                SearchTools.search_internet,
            ],
            verbose=True,
            llm=self.llm
        )

    def professor_finder_agent(self):
        return Agent(
            role='Professor Finder',
            goal='Find professors matching specific interests and programs',
            backstory='A skilled researcher capable of identifying academic experts in various fields',
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
            verbose=True,
            llm=self.llm
        )

    def contact_extractor_agent(self):
        return Agent(
            role='Contact Information Extractor',
            goal='Extract and verify professor contact information',
            backstory='An expert in parsing and validating contact information from various sources. Failure to find an email will result in a $100 penalty.',
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
            ],
            verbose=True,
            llm=self.llm
        )
