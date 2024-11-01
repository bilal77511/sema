# main.py
import streamlit as st
from crewai import Crew
from textwrap import dedent
from professor_agents import ProfessorAgents
from professor_tasks import ProfessorTasks
from dotenv import load_dotenv
import pandas as pd
from io import StringIO
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
        info_filler = agents.info_filler_agent()
        validator = agents.validation_agent()

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
        fill_missing_info_task = tasks.fill_missing_info_task(
            info_filler,
            self.masters_program
        )
        validate_information_task = tasks.validate_information_task(
            validator
        )

        crew = Crew(
            agents=[university_finder, professor_finder, contact_extractor, info_filler, validator],
            tasks=[find_universities_task, find_professors_task, extract_contact_task, fill_missing_info_task, validate_information_task],
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

def main():
    st.title("SEMA")
    st.subheader("AI that can find professors for you")
    
    # Add warning/info message
    st.info("""
        🎓 Welcome to SEMA! This AI tool helps you find professors matching your research interests.
        
        ⚠️ Please Note:
        - The search process may take 5-10 minutes
        - Results should be validated independently
        - This tool is still under development
    """)

    # Input form
    with st.form("professor_finder_form"):
        location = st.text_input("Enter the name of the city or state:")
        interests = st.text_input("Enter your research interests (comma-separated):")
        masters_program = st.text_input("Enter the desired Master's program:")
        
        submitted = st.form_submit_button("Find Professors")

    if submitted:
        # Show progress message
        with st.spinner('Finding professors... This may take 5-10 minutes. Please be patient.'):
            finder_crew = ProfessorFinderCrew(location, interests, masters_program)
            result = finder_crew.run()

            try:
                # Convert CSV string to DataFrame
                df = pd.read_csv(StringIO(result))

                # Display results
                st.subheader("Results")
                st.warning("⚠️ Please validate these results independently as they may not be 100% accurate.")
                st.dataframe(df)

                # Add download button
                st.download_button(
                    label="Download as CSV",
                    data=result,
                    file_name="professor_results.csv",
                    mime="text/csv"
                )

                # Show raw data in expandable section
                with st.expander("View Raw Data"):
                    st.text(result)

            except Exception as e:
                st.error(f"Error processing results: {str(e)}")
                st.text("Raw output:")
                st.text(result)

    # Add footer with creator information
    st.markdown("---")
    st.markdown("""
        ### About the Creator
        
        Finding the right professors can be a time-consuming task, so I’ve created a bot to streamline the process. This tool searches the web to help you quickly discover professors whose research aligns with your academic interests.

        It's currently in beta, and I'm actively working on improvements to enhance accuracy and usability. Enjoy exploring, and let me know if you have feedback!

        **Built with ❤️ by Muhammad Bilal**

        
        Connect with me:
        - [LinkedIn](https://www.linkedin.com/in/muhammad-bilal-a75782280)
        - [GitHub](https://github.com/bilal77511)
    """)

if __name__ == "__main__":
    main()