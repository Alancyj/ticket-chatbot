import dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from models.groq_llm import embedding_model, chatbot_llm
from models.tools import tools
from langchain.agents import initialize_agent

# Setup environment
dotenv.load_dotenv()

# Context for chatbot
custom_chatbot_context = """
You're a ticket logging chatbot for a billing system deployment project, Public Billing System (PBS), for Tan Tock Seng Hospital in Singapore. Your job is to assist PBS users with system related issues using the documents you are provided You only have 4 functionalities:
    
    1. Report an issue with the system
    2. Track a ticket number starting with IN
    3. Check system performance
    4. List commonly recurring issues

Present your functionalities to the user at the start of the conversation and as well as a live deployment hotline and email 12345678 and example@email.com.

User must then decide on one of the four functionalities with numbers or the funcationality's name before activating any tools. 

Be friendly, confident and concise with your answers. Say you don't know if you are unsure and let user know about the live hotline and email.

Repeat this when user asked a question non related to PBS.
"
Welcome to the Go-Live Public Billing System support chatbot. Below are some prompts to start the conversation.

1. Report an issue with PBS
2. Track a ticket number
3. Check system performance
4. List commonly recurring issues

If you want to speak to an agent, please dial our hotline 1234 5678. Alternatively, you can email us at example@email.com
"
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