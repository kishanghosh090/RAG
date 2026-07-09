from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient  # <-- Imported MongoClient
import os

load_dotenv()
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")


class State(TypedDict):
    """State of the chat session.""" 
    messages: Annotated[list, add_messages] 

def chatbot(state: State):
    print("we are inside chatbot node\n", state)
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}


graph_builder = StateGraph(State)

# build nodes
graph_builder.add_node("chatbot", chatbot)

# create edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


def compile_graph_with_checkpointer():
    client = MongoClient(os.getenv("MONGODB_URI"))
    
    checkpointer = MongoDBSaver(client, db_name="lg")
    
    # 3. Compile and return
    return graph_builder.compile(checkpointer=checkpointer)


graph_with_check_point = compile_graph_with_checkpointer()        

config = {
    "configurable": {
        "thread_id": "kishan"
    }
}

# First run: State initialization
updated_state = graph_with_check_point.invoke(
    {"messages": [{"role": "user", "content": "what is my name?"}]}, 
    config
)
print("--- FIRST RESPONSE ---")
print(updated_state["messages"][-1].content)


# 
