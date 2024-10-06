import os
import requests
import re
import json
from bs4 import BeautifulSoup
from langchain.tools import tool

class EmailSearchTool:
    @staticmethod
    def search_google(query):
        search_url = f"https://www.google.com/search?q={query}+email"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        potential_emails = soup.find_all(text=re.compile(email_pattern))
        
        if potential_emails:
            return re.search(email_pattern, potential_emails[0]).group(0)
        return None

    @staticmethod
    def search_serper(query):
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": f"{query} email"})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()

        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        for result in results.get('organic', []):
            snippet = result.get('snippet', '')
            match = re.search(email_pattern, snippet)
            if match:
                return match.group(0)
        return None

    @tool("Search for professor email")
    def search_professor_email(query):
        """
        Searches for a professor's email address using both Google and Serper.
        
        Args:
        query (str): A string containing the professor's name and university.
        
        Returns:
        str: The most likely email address found, or a message if no email was found.
        """
        email = EmailSearchTool.search_google(query)
        if not email:
            email = EmailSearchTool.search_serper(query)
        
        return email if email else "No email address found for the given professor and university."
