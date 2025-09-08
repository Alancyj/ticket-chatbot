from langchain_intro.chatbot import ticket_chatbot_agent
from langchain_core.messages import AIMessage, HumanMessage
from messages import appMessages

# Chatbot history
all_messages = []
all_messages.append(AIMessage(content=appMessages.messageStartUp))

def call_model(query):
    result = ticket_chatbot_agent.invoke(query)

    return result["output"]

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
    print(AIResponse)