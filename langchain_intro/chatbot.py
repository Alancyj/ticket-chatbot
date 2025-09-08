from langchain_groq import ChatGroq
import dotenv
from messages import appMessages
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough
from langchain_intro.embedding_model import embedding_model


dotenv.load_dotenv()

chatbot_template_str = """

You are a ticket logging chatbot for this billing system project deployment in Singapore for all Public Healthcare Instituitions. Hospital users will come to you for any system related issue, you will assist them in either suggesting similar incidents base on their issue description or assist them to log a ticket. When the human prompts "/start", you will return the main menu:
start off with
Good [Morning/Evening/Night] based on the time of day, then follow by this (word for word):
"
    Welcome to the Go-Live National Billing System support chatbot. Below are some prompts to start the conversation.

    1. Report an issue with NBS
    2. Track a ticket number
    3. Checking system performance
    4. Top reported issues

    If you want to speak to an agent, please dial our hotline [NBS deployment hotline]. Alternatively, you can email us at [NBS deployment email]
"

Let them know they can quit the chatbot by saying the commands "/quit" or "/exit".

If you are not sure about a user query, say you don't know.

{context}
"""

REVIEWS_CHROMA_PATH = "chroma_data/"

chatbot_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=[
        SystemMessagePromptTemplate.from_template(chatbot_template_str),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ],
)

chat_model = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    # other params...
)

incident_vector_db = Chroma(
    persist_directory=REVIEWS_CHROMA_PATH,
    embedding_function=embedding_model,
)

incident_retriever  = incident_vector_db.as_retriever(k=10,search_type="similarity")

chatbot_chain = (
    {
        "context": lambda x: incident_retriever.invoke(x["question"]),
        "question": lambda x: x["question"],
        "chat_history": lambda x: x.get("chat_history", []),
    }
    | chatbot_prompt_template
    | chat_model
    | StrOutputParser()
)