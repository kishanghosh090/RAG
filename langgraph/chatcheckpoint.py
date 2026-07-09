from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

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


graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": "hi my name is kishan rana ghosh"}))
print(updated_state)

