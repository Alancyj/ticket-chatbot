# WITHOUT PROMPT TEMPLATE

from langchain.schema.messages import HumanMessage, SystemMessage
from langchain_intro.chatbot import chat_model

messages = [
    SystemMessage(
        content="""You're an assistant knowledgeable about
        healthcare. Only answer healthcare-related questions."""
    ),
    HumanMessage(content="How do I change a tire?"),
]

out = chat_model.invoke(messages).content # out is the output of the chat_model, * content key is the msg body


print(out)
