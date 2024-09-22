from crewai import Task
from textwrap import dedent

class ProfessorTasks:

    def find_universities_task(self, agent, location):
        return Task(
            description=dedent(f"""
                Find all public research universities located in {location}.
                Provide a list of university names along with their main websites.
                Ensure that you find at least as many universities as there will be professors to search for.

                Your final answer should be a list of public research universities and their websites.
            """),
            agent=agent,
            expected_output="List of public research universities and their websites in the specified location"
        )

    def find_professors_task(self, agent, interests, masters_program):
        return Task(
            description=dedent(f"""
                For each public research university provided, find one professor whose research interests 
                align with {interests} and who is associated with the {masters_program} program.
                Provide the professor's name, their specific research interests, and the university they belong to.
                Ensure that you find exactly one professor per university.

                Your final answer should be a list of professors, their research interests, and their universities.
            """),
            agent=agent,
            expected_output="List of professors, their research interests, and their universities"
        )

    def extract_contact_task(self, agent):
        return Task(
            description=dedent(f"""
                For each professor identified, extract their email address from the university website or faculty page.
                Verify that the extracted email is likely to be correct (e.g., matches the professor's name,
                follows typical university email formats).
                Remember, failing to find an email will result in a $100 penalty, so make sure to exhaust all possible sources.

                Your final answer should be a json output containing each professor's name, email address, 
                university, research interests and available master programs at their univerity with regards to my interests. If an email cannot be found after extensive searching,
                clearly state "Email not found" for that professor.
            """),
            agent=agent,
            expected_output="List of professors with their name, email (or 'Email not found'), university, research interests, available master programs at their university. I want the final output in proper json format."
        )
