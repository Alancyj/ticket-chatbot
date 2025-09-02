# WITH PROMPT TEMPLATE
# REVIEW CHAIN - INCLUDES CONTEXT

from langchain_intro.chatbot import review_chain

context = "I had a great stay!"
question = "Did anyone have a positive experience?"

out = review_chain.invoke({"context": context, "question": question})

print(out.content)

