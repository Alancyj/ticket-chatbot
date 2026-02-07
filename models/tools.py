import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

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
# Function 1.a, retrieve similar incidents
def retrieve_similar_incidents(input=""):

    incident_retriever = incident_vector_db.as_retriever(k=2,search_type="similarity").invoke(input)

    return incident_retriever

# Activate criteria
retrieve_incident_func = Tool(
    name='To search similar incidents',
    func= retrieve_similar_incidents,
<<<<<<< HEAD
    description="This is the first function of the chatbot. Do not use this tool if the suggested resolution is not helping the user or does not solve their issue. Useful for when you need to find similar incidents. Summarise the output of the tool if exists. If user did not include description of issue, do not suggest any past issues, tell them provide an issue description. "
=======
    description="Useful for when you need to find similar incidents. Summarise the output of the tool if exists. If user did not include description of issue, do not suggest any past issues, tell them to provide an issue description."
>>>>>>> 750dab8eeff527424c6d11d05794918f99a85574
)


# Function 1.b, send reporting template
def send_reporting_template(input=""): return
send_reporting_template_func = Tool(
    name='To send issue reporting template/form',
    func= send_reporting_template,
<<<<<<< HEAD
    description= """This is the first function of the chatbot. Do not use this tool if user has not described their issue. If after describing user issue, and the suggested solution did not help the user. Say exactly this 'Fill Issue Reporting Form'"""
)

# Function 2, send auth form
def send_auth_template(input=""): return
send_auth_template_func = Tool(
    name='To send issue authorisation template/form',
    func= send_auth_template,
    description= """If user wants to fill up the authorisation template/form. say exactly this 'Fill Authorisation Form'"""
)

# Function 3, track a ticket number
=======
    description= "If user wants to fill up the issue reporting template/form. say exactly this 'Fill Issue Reporting Form'"
)


# Function 2, track a ticket number
>>>>>>> 750dab8eeff527424c6d11d05794918f99a85574
def search_ticket_number(input=""):
    fpath = "models/data/ttsh_golive_incidents_mockup_v3.csv"
    
    table = pd.read_csv(fpath)
    incident_row = table[table["Incident Number"] == input]
    s = ''
    if len(incident_row) > 0:
        for x,y in zip(table.columns, incident_row.iloc[0]):
            s += f'{x}: {y}, '

    return s

# Activate criteria
search_ticket_func = Tool(
    name='To search ticket number',
    func= search_ticket_number,
    description="If the user provides a ticket number starting with IN and followed by exactly 7 digits, Send the tool's output if exists, including the description and status. If the status is closed, include the incident resolution and date closed as well. Else in all cases, say 'Please type the ticket number you want to track.'"
)

<<<<<<< HEAD
=======

>>>>>>> 750dab8eeff527424c6d11d05794918f99a85574
# Function 4, list commonly recurring issues
def list_common_issues(input=""):
    fpath = "models/data/ntfh_golive_incidents_mockup_v1.csv"
    
    table = pd.read_csv(fpath)
    table = table[table['Status'] != 'RESOLVED'] # only show users common issues that are unresolved

    return table

# Activate criteria
list_common_issues_func = Tool(
    name='To list commonly recurring issues',
    func= list_common_issues,
    description="Useful for finding commonly recurring issues. Summarise the top three common issues according to the Incident Title column. If user asks you to elaborate on or explain any one of the issues, include the incident description in your elaboration and explanation of the issue(s)."
)

<<<<<<< HEAD
=======

>>>>>>> 750dab8eeff527424c6d11d05794918f99a85574
# Corner popup, checking system status
def check_system_status(input=""):
    """
    Manually updated in the backend.

    [currently down/experiencing slowness/experiencing extreme slowness/normal]
    """

    system_status =  "Normal"

    x = datetime.datetime.now()

    last_updated = x.strftime("%c") #e.g. output, Mon Sep 08 11:26:27 2025

    return f"{system_status}. Last updated: {last_updated}"

# List will be passed to chatbot agent to use
<<<<<<< HEAD
tools = [search_ticket_func, retrieve_incident_func, send_reporting_template_func, send_auth_template_func, list_common_issues_func]
# tools = [search_ticket_func, send_reporting_template_func, send_auth_template_func, list_common_issues_func]
=======
tools = [search_ticket_func, retrieve_incident_func, send_reporting_template_func, list_common_issues_func]
tools = [search_ticket_func, send_reporting_template_func, list_common_issues_func]
>>>>>>> 750dab8eeff527424c6d11d05794918f99a85574
