import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from utils import read_file, get_table_data
from logger import logging
from MCQ_GENERATOR import generate_evaluate_chain
import streamlit as st

# Load JSON data
try:
    with open("/home/saurabh_kokare/Music/APP/myenv/Response.json", 'r') as file:
        RESPONSE_JSON = json.load(file)
except FileNotFoundError:
    st.error("Response.json file not found. Please check the file path.")
    RESPONSE_JSON = None
except json.JSONDecodeError as e:
    st.error(f"Error decoding JSON: {e}")
    RESPONSE_JSON = None

# Streamlit title
st.title("MCQ Generator App Using Langchain")

# Form for user inputs
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or TXT file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Enter Subject name", max_chars=50)
    tone = st.text_input("Complexity Level of Questions", max_chars=50, placeholder="simple")
    button = st.form_submit_button("Create MCQs")

    if button:
        if uploaded_file is None:
            st.error("Please upload a valid file.")
        elif not subject.strip():
            st.error("Please enter a subject name.")
        elif not tone.strip():
            st.error("Please specify the complexity level.")
        elif RESPONSE_JSON is None:
            st.error("Response.json could not be loaded. Check the file path and content.")
        else:
            with st.spinner("Processing..."):
                try:
                    # Extract text from the uploaded file
                    text = read_file(uploaded_file)
                    if not text:
                        raise ValueError("The uploaded file contains no readable text.")

                    # Generate MCQs
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON),
                    })

                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
                    st.error(f"An error occurred: {e}")
                else:
                    # Process and display quiz
                    quiz = response.get("quiz", None)
                    if quiz is None:
                        st.error("The 'quiz' key is missing or empty in the response.")
                    else:
                        st.write("Generated Quiz:",quiz)
                        #st.json(quiz)  # Display quiz as JSON for better readability
