import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from utils import read_file,get_table_data
from logger import logging
import cohere
load_dotenv()

cohere_api_key=os.environ['COHERE_API_KEY']

co = cohere.ClientV2(api_key=cohere_api_key)

from langchain_cohere import ChatCohere

llm = ChatCohere(model="command-r")

from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import PromptLayerCallbackHandler
import PyPDF2

RESPONSE_JSON={
    "1":{
        "mcq":"multiple choice question",
        "options":{
            "a":"choice here",
            "b":"choice here",
            "c":"choice here",
            "d":"choice here"
        },
        "correct":"correct answer",
    },
    "2":{
        "mcq":"multiple choice question",
        "options":{
            "a":"choice here",
            "b":"choice here",
            "c":"choice here",
            "d":"choice here"
        },
        "correct":"correct answer",
    },
    "3":{
        "mcq":"multiple choice question",
        "options":{
            "a":"choice here",
            "b":"choice here",
            "c":"choice here",
            "d":"choice here"
        },
        "correct":"correct answer",
    },
    "4":{
        "mcq":"multiple choice question",
        "options":{
            "a":"choice here",
            "b":"choice here",
            "c":"choice here",
            "d":"choice here"
        },
        "correct":"correct answer",
    },
    "5":{
        "mcq":"multiple choice question",
        "options":{
            "a":"choice here",
            "b":"choice here",
            "c":"choice here",
            "d":"choice here"
        },
        "correct":"correct answer",
    }
}

TEMPLATE="""
    Text:{text}
    You are an expert MCQ maker.Given the above text it is your job \
    to create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
    make sure the questions are not repeated and check all the questions to be conforming the text as well.
    make sure to format your response like RESPONSE_JSON below and use it as guide.\
    Ensure to make {number} MCQs
    ###RESPONSE_JSON
    {response_json}
    
    
"""

quiz_generation_prompt=PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=TEMPLATE    
)

quiz_chain=LLMChain(llm=llm,prompt=quiz_generation_prompt,output_key="quiz")

TEMPLATE2="""
    You are an expert english grammarian and writer.Given a multiple choice quiz for {subject} students.\
    You need to evaluate complexity of the question and give a complete analysis of quiz.only use at max 50 words.
    If the quiz is not as per with the cognitive and analytical abilities of the students.\
    update the quiz questions which need to be changed and change the tone such that it perfectly fits.
    Quiz_MCQs:
    {quiz}
    
    Check from an expert english writer of the above quiz:

"""

callback = PromptLayerCallbackHandler()

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject","quiz"],template=TEMPLATE,callbacks=[callback])

review_chain=LLMChain(llm=llm,prompt=quiz_evaluation_prompt,output_key="review",verbose=True)

generate_evaluate_chain=SequentialChain(
    chains=[quiz_chain,review_chain],input_variables=["text","number","subject","tone","response_json"],
    output_variables=["subject","quiz"],verbose=True,
    
)