from crewai import Task
from textwrap import dedent

class ProfessorTasks:

    def find_universities_task(self, agent, location):
        return Task(
            description=dedent(f"""
                Find all public research universities located in {location}.
                if the {location} is in USA U can use collegevine.com
                Provide a list of public research universities names along with their main websites.
                Validate the results

                Your final answer should be a list of public research universities and their websites.
            """),
            agent=agent,
            expected_output="List of public research universities in the specified location"
        )

    def find_professors_task(self, agent, interests, masters_program):
        return Task(
            description=dedent(f"""
                For each public research university provided, find one professor whose research interests align with {interests}.
                For each public research university Provide the professor's name, their specific research interests, and the university they belong to.
                Ensure that you find exactly one professor per university.
                The number of universities should be equal to the number of professors.
                Validate all the information.
                Your final answer should be a list of professors, their research interests, and their universities. 
            """),
            agent=agent,
            expected_output="Name of universities, list of professors, their research interests"
        )

    def extract_contact_task(self, agent):
        return Task(
            description=dedent(f"""
                For each professor identified, extract their education email address using google with queries like [universityname professorname emailadress] or any other method.
                you can use google with queries like [universityname professorname emailadress]
                For each professor verify that the extracted email is correct by cross-referencing.
                If multiple email addresses are found, prioritize .edu or official university domain emails.
                validate all the information using google 
            """),
            agent=agent,
            expected_output="A list of professors, their verified email addresses, name of university, professor research interests"
        )

    def fill_missing_info_task(self, agent, masters_program):
        return Task(
            description=dedent(f"""
                Review the collected professors information. For any missing fields, attempt to find the information.
                Find all master programs or graduate programs offered by each university in department{masters_program}.
                Ensure all fields are present for each professor: name, email, university, department, research interests, and master programs. 
                Verify the name, email, university, and research interest of each professor is correct.
                Validate all the data using google.
                Your final answer should be a complete JSON output with all available information for each professor.
            """),
            agent=agent,
            expected_output="Complete JSON output about professor: name, email, university, department, research interests, and master programs."
        )
    def validate_information_task(self, agent):
        return Task(
            description=dedent(f"""
                Thoroughly validate all the information collected about professors and universities.
                This includes:
                1. Verifying the existence and status of each university as a public research institution.
                2. Confirming each professor's email adress is correct if not present look for it search on google .
                4. Validating email addresses by checking official university directories or contact pages or google .
                5. Confirming the existence of the mentioned master's programs at each university.

                

                Your final answer should be a complete JSON output with all available information for each professor.
            
            """),
            agent=agent,
            expected_output="Complete validated JSON output about professor: name, email, university, department, research interests, and master programs."
        )
