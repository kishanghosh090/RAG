from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    """State of the chat session.""" 
    messages: Annotated[list, add_messages] 

def chatbot(state: State):
    print("we are inside chatbot node\n", state)
    return {"messages": ["Hello! How can I assist you today?"]}

def sample_node(state: State):
    print("we are inside sample node\n", state)
    return {"message": ["sample message appended"]}

graph_builder = StateGraph(State)

# build nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample_node", sample_node)

# create edges

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sample_node")
graph_builder.add_edge("sample_node", END)


graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": "hi my name is kishan rana ghosh"}))
print(updated_state)

