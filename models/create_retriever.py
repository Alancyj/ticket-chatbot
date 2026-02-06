import os
import dotenv
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from groq_llm import embedding_model

from transformers import AutoModel
from langchain.text_splitter import RecursiveCharacterTextSplitter



REVIEWS_CSV_PATH = "./data/ttsh_golive_incidents_mockup_v3.csv"
REVIEWS_CHROMA_PATH = "./chroma_data2"

# SETUP
dotenv.load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

# LOAD DATA
loader = CSVLoader(file_path=REVIEWS_CSV_PATH, source_column="Incident Title")
reviews = loader.load()

# STORE INTO 
vector_store = Chroma.from_documents(reviews, embedding_model, persist_directory=REVIEWS_CHROMA_PATH)
vector_store