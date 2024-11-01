# main.py
import streamlit as st
from crewai import Crew
from textwrap import dedent
from professor_agents import ProfessorAgents
from professor_tasks import ProfessorTasks
from dotenv import load_dotenv
import pandas as pd
from io import StringIO

load_dotenv()

class ProfessorFinderCrew:

    def __init__(self, location, interests, masters_program):
        self.location = location
        self.interests = interests
        self.masters_program = masters_program

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

        return crew.kickoff()

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
                # Convert CSV string to DataFrame with proper parsing
                df = pd.read_csv(
                    StringIO(result),
                    names=['Name', 'Email', 'University', 'Department', 'Research Interests', 'Programs'],  # Define column names
                    quoting=1,  # Handle quoted fields
                    doublequote=True,  # Handle double quotes
                    escapechar=None,
                    on_bad_lines='warn'
                )

                # Clean up any potential whitespace
                df = df.apply(lambda x: x.str.strip() if isinstance(x, str) else x)

                # Display results
                st.subheader("Results")
                st.warning("⚠️ Please validate these results independently as they may not be 100% accurate.")
                
                # Display DataFrame with better formatting
                st.dataframe(
                    df,
                    column_config={
                        "Name": st.column_config.TextColumn("Professor Name"),
                        "Email": st.column_config.TextColumn("Email Address"),
                        "University": st.column_config.TextColumn("University"),
                        "Department": st.column_config.TextColumn("Department"),
                        "Research Interests": st.column_config.TextColumn("Research Interests"),
                        "Programs": st.column_config.TextColumn("Available Programs")
                    },
                    hide_index=True
                )

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