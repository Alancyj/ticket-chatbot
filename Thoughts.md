ref guide https://realpython.com/build-llm-rag-chatbot-with-langchain/#step-1-get-familiar-with-langchain
ref guide for groq https://groq.com/blog/retrieval-augmented-generation-with-groq-api
chromadb https://www.trychroma.com/yeejiealan1/Production/sdk
Huggingface (embedding model) https://huggingface.co/models
git https://github.com/Alancyj/ticket-chatbot
designing context of chatbot https://www.chatmetrics.com/blog/best-practices-for-chatbot-context-design

steps so far:

1. Create basic langchain model - answer questions using llm, with a custom chatbot ie., healthcare assistant, see run1.py

2. In langchain, can manually pass context - able to answer questions using chain from past knowledge, ie., data/context, see run2.py

3. The goal of review_chain is to answer questions about patient experiences in the hospital from their reviews. So far, you’ve manually passed reviews in as context for the question. While this can work for a small number of reviews, it doesn’t scale well. Moreover, even if you can fit all reviews into the model’s context window, there’s no guarantee it will use the correct reviews when answering a question.

To overcome this, you need a retriever. The process of retrieving relevant documents and passing them to a language model to answer questions is known as retrieval-augmented generation (RAG).

For this example, you’ll store all the reviews in a vector database called ChromaDB. If you’re unfamiliar with this database tool and topics, then check out Embeddings and Vector Databases with ChromaDB before continuing.