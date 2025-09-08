from langchain_intro.chatbot import chatbot_chain
from langchain_core.messages import AIMessage, HumanMessage
from messages import appMessages

# Chatbot history
all_messages = []
all_messages.append(AIMessage(content=appMessages.messageStartUp))

def call_model(query, history):
    # Call the chatbot_chain with the current question and chat history
    result = chatbot_chain.invoke({
        "question": query,
        "chat_history": all_messages  
    })

    # Add user/AI message to chat history
    all_messages.append(HumanMessage(content=query))
    all_messages.append(AIMessage(content=result))

    return result, history

result, all_messages = call_model("/start", all_messages)    
print(result)


while True:
    # Input

    user_input = input(">>>> ")
    all_messages.append(HumanMessage(content=user_input))

    # Return to main menu
    if user_input.lower() in {"/exit", "/quit"}:
        break

    result, all_messages = call_model(user_input, all_messages)    
    print(
        result
        )






# # Run app
# while True:
#     user_input = input(">>>> ")
#     all_messages.append(HumanMessage(content=user_input))
    
#     # Exit
#     if user_input.lower() in {"exit", "quit"}:
#         break

#     # Return to main menu
#     if user_input.lower() in {"restart"}:
#         print(appMessages.messageStartUp)
#         all_messages.append(AIMessage(content=appMessages.messageStartUp))

#     match user_input:
#         case "1":
#             # Report an issue with NBS
#             while True:
#                     # Output

#                 # Return to main menu
#                 if user_input.lower() in {"restart"}:
#                     break

#                 user_query = input("Please describe your issue \n>>>> ")

#                 result, all_messages = call_model(user_query, all_messages)    
#                 print(
#                     result, 
#                     "\n\n",
#                     appMessages.messageLastAI
#                     )
                
#         case "2":
#             # Track a ticket number
#             print("This is 2")
#         case "3":
#             # Checking system performance
#             print("This is 3")
#         case "4":
#             # Top reported issues
#             print("This is 4")



