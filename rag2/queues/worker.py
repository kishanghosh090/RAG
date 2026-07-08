import os
from functools import lru_cache
from openai import OpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()


@lru_cache(maxsize=1)
def _get_openai_client() -> OpenAI:
    return OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/")


@lru_cache(maxsize=1)
def _get_vector_db():
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2",
        google_api_key=os.getenv("OPENAI_API_KEY"),
    )
    return QdrantVectorStore.from_existing_collection(
        url=os.getenv("QDRANT_URL"),
        embedding=embedding_model,
        collection_name="learning_rag",
    )


def process_query(query: str):
    print(f"Processing query: {query}")
    vector_db = _get_vector_db()
    client = _get_openai_client()
    search_result = vector_db.similarity_search(query=query)
    context = "\n\n\n".join([f"page content {result.page_content}\n Page Number : {result.metadata['page']}\nFile Location {result.metadata['source']}" for result in search_result])

    SYSTEM_PROMPT = f"""
    you are a helpful AI assistant who answer user query based on available contxt retrived from a PDF file page_contents and page numbers.

    you should only anser the user based on the following context and navigate the user to open the right page number to know more.

    context:
        
    {context}
    """
    res = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    print(res.choices[0].message.content)
    return res.choices[0].message.content




