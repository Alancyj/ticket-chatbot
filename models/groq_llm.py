from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
import dotenv

dotenv.load_dotenv()

embedding_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

# LLM
# Token limit of 10000
chatbot_llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
)

