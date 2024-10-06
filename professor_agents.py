from crewai import Agent
from langchain_openai import ChatOpenAI
from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
from tools.email_search_tool import EmailSearchTool
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
            role='Email Extractor',
            goal='Extract and verify professor email addresses',
            backstory='An expert in finding and validating email addresses',
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
                EmailSearchTool.search_professor_email,
            ],
            verbose=True,
            llm=self.llm
        )

    def info_filler_agent(self):
        return Agent(
            role='Information Filler',
            goal='Fill in missing professor information',
            backstory='A meticulous researcher capable of finding and verifying academic information from official sources or Google',
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
                EmailSearchTool.search_professor_email,
            ],
            verbose=True,
            llm=self.llm
        )
    def validation_agent(self):
        return Agent(
            role='Information Validator',
            goal='Validate all collected information about professors and universities',
            backstory='A meticulous fact-checker with expertise in academic information verification',
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
                EmailSearchTool.search_professor_email,
            ],
            verbose=True,
            llm=self.llm
        )