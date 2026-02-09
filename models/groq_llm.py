from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
import dotenv

dotenv.load_dotenv()

# Lazy-load embeddings
embedding = None
def get_embedding():
    embedding_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

    return embedding_model

embedding_model = get_embedding()

# Lazy-load LLM
_llm_instance = None
def get_chatbot_llm():
    global _llm_instance
    if _llm_instance is None:
        print("Loading ChatGroq LLM...")
        _llm_instance = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
    return _llm_instance

chatbot_llm = get_chatbot_llm()