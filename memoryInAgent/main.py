from mem0 import Memory
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  


API_KEY = os.environ.get("GOOGLE_API_KEY") or ""
client = OpenAI(api_key=API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
import json
config = {
    "version": "v1.1",
    "llm": {
        "provider": "gemini",  # Changed to 'gemini'
        "config": {
            "model": "gemini-3.1-flash-lite",
            "api_key": API_KEY,
        }
    },
    "embedder": {
        "provider": "gemini",  # Changed to 'gemini'
        "config": {
            "model": "gemini-embedding-2",
            "api_key": API_KEY,
                "embedding_dims": 1536 
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "13.204.134.210",
            "port": 6333,
             "collection_name": "mem0_gemini_v2"
        }
    }
}

mem_client = Memory.from_config(config)

user_query = input("Enter your query: ")

search_results = mem_client.search(query=user_query, user_id="kishan")
memory_about_user = search_results

memories = [
    f"ID {mem.get("id")}\nMemory: {mem.get("memory")}" for mem in memory_about_user
]
SYSTEM_PROMPT = f"""
You are a helpful assistant that uses the following memories to answer the user's query.
Memories:
{json.dumps(memories, indent=2)}
"""

res = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[
        {
            "role": "system", "content": SYSTEM_PROMPT,
        
            "role": "user", "content": user_query}
    ],
)
ai_response = res.choices[0].message.content
print("AI Response:", ai_response)

mem_client.add(
    user_id="kishan",
    messages=[
        {"role": "user", "content": user_query},
        {"role": "assistant", "content": ai_response}
    ]
)
print("memory added successfully.")