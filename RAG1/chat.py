from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)



vector_db = QdrantVectorStore.from_existing_collection(
        url=os.getenv("QDRANT_URL"),
        embedding=embedding_model,
        collection_name="learning_rag",
    )


# take user input 
user_query = input("Ask something > ")

# relevet chunks from vector db
search_result = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join([f"page content {result.page_content}\n Page Number : {result.metadata['page']}\nFile Location {result.metadata["source"]}" for result in search_result])

# print(context)
SYSTEM_PROMPT = f"""
    you are a helpful AI assistant who answer user query based on available contxt retrived from a PDF file page_contents and page numbers.

    you should only anser the user based on the following context and navigate the user to open the right page number to know more.

    context:
        {context}

"""

client = OpenAI(
    api_key= os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

res = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[
        {'role': "system", 'content': SYSTEM_PROMPT},
        {'role': "user", "content": user_query}
    ]
)

print(res.choices[0].message.content)