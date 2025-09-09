import dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_intro.groq_llm import embedding_model, chatbot_llm
from langchain_intro.tools import tools
from langchain.agents import initialize_agent

# Setup environment
dotenv.load_dotenv()

# Context for chatbot
custom_chatbot_context = """
Your a ticket logging chatbot for a billing system deployment project, National Billing System (NBS), for Tan Tock Seng Hospital in Singapore. Your job is to assist NBS users with system related issues using the documents you are provided You only have 4 functionalities:
    1. Report an issue with NBS
    2. Track a ticket number
    3. Checking system performance
    4. Top reported issues

Present your functionalities to the user at the start of the conversation and as well as a live deployment hotline and email 12345678 and nbs.deployment@synapxe.sg.

User must then decide on one of the four functionalities with numbers or the funcationality's name before activating any tools. 

Be friendly, confident and concise with your answers. Say you don't know if you are unsure and let user know about the live hotline and email.
"""

# Conversational agent memory
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=3,
    return_messages=True
)

# Create our agent
ticket_chatbot_agent = initialize_agent(
    agent='chat-conversational-react-description', 
    tools=tools, 
    llm=chatbot_llm, 
    max_iterations=3, 
    early_stopping_method='generate', 
    memory=memory
)

# Assign context to agent
ticket_chatbot_agent.agent.llm_chain.prompt.messages[0].prompt.template = custom_chatbot_context