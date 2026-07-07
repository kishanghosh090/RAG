import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_qdrant import QdrantVectorStore

load_dotenv()


pdf_path = Path(__file__).parent / "passbook.pdf"

# load document page by page

loader = PyMuPDFLoader(str(pdf_path))
documents = loader.load()

print(f"Loaded {len(documents)} pages")


# Split Documents


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")


# Gemini Embedding 

# embeddings = OpenAIEmbeddings(
#     model="gemini-embedding-001",
#     api_key=os.getenv("GEMINI_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)
# Store in Qdrant

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url=os.getenv("QDRANT_URL"),
    collection_name="learning_rag",
    batch_size=50,

)

# print("✅ Document indexed successfully!")