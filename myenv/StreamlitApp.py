import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from utils import read_file,get_table_data
from logger import logging
from MCQ_GENERATOR import generate_evaluate_chain
import cohere
import streamlit as st

with open("/home/saurabh_kokare/Music/APP/myenv/Response.json",'r') as file:
    RESPONSE_JSON=json.load(file)
    
st.title("MCQ Generator App Using Langchain")

with st.form("user_inputs"):
    uploaded_file=st.file_uploader("Upload a pdf or txt file")
    
    mcq_count=st.number_input("No. of MCQs",min_value=3,max_value=50)
    
    subject=st.text_input("Enter Subject name",max_chars=50)
    
    tone=st.text_input("Complexity Level of Questions",max_chars=50,placeholder="simple")
    
    button=st.form_submit_button("Create MCQs")
    
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
            
                response=generate_evaluate_chain(
                    {
                        "text":text,
                        "number":mcq_count,
                        "subject":subject,
                        "tone":tone,
                        "response_json":json.dumps(RESPONSE_JSON)
                    }
                
                )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
        
            else:
                quiz = response.get("quiz", None)
                if quiz is None:
                    st.error("The 'quiz' key is missing or empty in the response.")
                else:
                    st.write(quiz)  # Display the quiz content
