import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
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
    chunk_size=1000,
    chunk_overlap=100,
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")


# Gemini Embedding 


# embedding_model = OpenAIEmbeddings(
#     model="text-embedding-3-large",
# )
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    google_api_key=os.getenv("OPENAI_API_KEY"),
)
# Store in Qdrant

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url=os.getenv("QDRANT_URL"),
    collection_name="learning_rag",
)

print("✅ Document indexed successfully!")