from crewai import Crew
from textwrap import dedent
from professor_agents import ProfessorAgents
from professor_tasks import ProfessorTasks
from dotenv import load_dotenv
import json
import os

load_dotenv()

class ProfessorFinderCrew:

    def __init__(self, location, interests, masters_program):
        self.location = location
        self.interests = interests
        self.masters_program = masters_program
        self.data_file = 'professor_data.json'
        self.output_file = 'professor_results.txt'

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self, data):
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def save_output(self, result):
        with open(self.output_file, 'w') as f:
            f.write(result)

    def run(self):
        agents = ProfessorAgents()
        tasks = ProfessorTasks()

        university_finder = agents.university_finder_agent()
        professor_finder = agents.professor_finder_agent()
        contact_extractor = agents.contact_extractor_agent()

        find_universities_task = tasks.find_universities_task(
            university_finder,
            self.location
        )
        find_professors_task = tasks.find_professors_task(
            professor_finder,
            self.interests,
            self.masters_program
        )
        extract_contact_task = tasks.extract_contact_task(
            contact_extractor
        )

        crew = Crew(
            agents=[university_finder, professor_finder, contact_extractor],
            tasks=[find_universities_task, find_professors_task, extract_contact_task],
            verbose=True
        )

        result = crew.kickoff()

        # Save the result to local storage
        data = self.load_data()
        if self.location not in data:
            data[self.location] = {}
        data[self.location][self.masters_program] = result
        self.save_data(data)

        # Save the result to a text file
        self.save_output(result)

        return result

if __name__ == "__main__":
    print("## Welcome to Professor Finder")
    print('-----------------------------')
    location = input("Enter the name of the city or state: ")
    interests = input("Enter your research interests (comma-separated): ")
    masters_program = input("Enter the desired Master's program: ")
    
    finder_crew = ProfessorFinderCrew(location, interests, masters_program)
    result = finder_crew.run()
    print("\n\n########################")
    print(f"## Professor Details have been saved to {finder_crew.output_file}")
    print("########################\n")
    print(result)
