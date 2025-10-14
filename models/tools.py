from langchain.agents import Tool
import pandas as pd
from langchain_community.vectorstores import Chroma
from models.groq_llm import embedding_model
import datetime

# Instantiate vector datebase 
REVIEWS_CHROMA_PATH = "chroma_data/"

incident_vector_db = Chroma(
    persist_directory=REVIEWS_CHROMA_PATH,
    embedding_function=embedding_model,
)

# Start of tools
# Function 1, retrieve similar incidents
def retrieve_similar_incidents(input=""):

    incident_retriever = incident_vector_db.as_retriever(k=5,search_type="similarity").invoke(input)

    return incident_retriever

# Activate criteria
retrieve_incident_func = Tool(
    name='To search similar incidents',
    func= retrieve_similar_incidents,
    description="Useful for when you need to finding similar incidents. Summarise the output of the tool if exists."
)

# Function 2, track a ticket number
def search_ticket_number(input=""):
    fpath = "models/data/ttsh_golive_incidents_mockup_v2.csv"
    
    table = pd.read_csv(fpath)
    incident_row = table[table["Incident Number"] == input]
    return incident_row

# Activate criteria
search_ticket_func = Tool(
    name='To search ticket number',
    func= search_ticket_number,
    description="If user enters a ticket number that does not start with IN, prompt them for a valid ticket number. Only use this tool if the ticket number provided starts with 'IN'. Useful for when you need to answer questions when tracking ticket number. Summarise the output of the tool if exists."
)

# Function 3, check system performance
def check_system_performance(input=""):
    """
    Manually updated in the backend.

    [currently down/experiencing slowness/experiencing extreme slowness/normal]
    """

    system_status =  "Normal"

    x = datetime.datetime.now()

    last_updated = x.strftime("%c") #e.g. output, Mon Sep 08 11:26:27 2025

    return f"{system_status}. Last updated: {last_updated}"

# Activate criteria
check_system_status_func = Tool(
    name='To return current system performance',
    func= check_system_performance,
    description="Useful for when you need to answer questions about National Billing System (NBS) system performance. "
)

# List will be passed to chatbot agent to use
tools = [search_ticket_func, retrieve_incident_func, check_system_status_func]

