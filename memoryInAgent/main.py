from mem0 import Memory
import os
config = {
    "version": "v1.1",
    "llm": {
        "provider": "google",
        "config": {
            "model": "gemini-2.0-flash-001",
            "api_key": os.environ.get("GOOGLE_API_KEY"),
        }
    },
    "embedder": {
        "provider": "google",
        "config": {
            "model": "models/gemini-embedding-001",
            "api_key": os.environ.get("GOOGLE_API_KEY"),
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "13.204.134.210",
            "port": 6333,
        }
    }
}



mem_client = Memory.from_config(config)