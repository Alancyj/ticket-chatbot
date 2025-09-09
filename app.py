from langchain_intro.chatbot import ticket_chatbot_agent
from groq import GroqError
from langchain_core.messages import AIMessage, HumanMessage
from messages import appMessages

# Chatbot history
all_messages = []
all_messages.append(AIMessage(content=appMessages.messageStartUp))

def call_model(query):
    try:
        result = ticket_chatbot_agent.invoke(query)

        return result["output"]
    except GroqError as e: # 
        if "rate limit" in str(e).lower():
            rate_limit_error = ("Opps, seems like rate limit reached. This error is occuring as we are using the free version of Groq model in this prototype/test.")

        return rate_limit_error

AIResponse = call_model("Start of conversation")    
print(AIResponse)


while True:
    # Input
    user_input = input(">>>> ")
    all_messages.append(HumanMessage(content=user_input))

    # Return to main menu
    if user_input.lower() in {"/exit", "/quit"}:
        break

    AIResponse = call_model(user_input)    
    print("\n**Chatbot Response**\n",AIResponse, sep='')