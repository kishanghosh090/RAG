from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

load_dotenv()
client = OpenAI(  base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    if_good: Optional[bool]


def chatbot(state: State):
   res =  client.chat.completions.create(model="gemini-2.5-flash", messages=[
        {"role": "user", "content": state.get("user_query") }
    ])
   
   state["llm_output"] = res.choices[0].message.content
   return state

def evaluate_response(state: State) -> Literal["chatbot_gemini_lite", "endnode"]:
    if False:
        return "endnode"
    
    return "chatbot_gemini_lite"


def chatbot_gemini_lite(state: State):
   res =  client.chat.completions.create(model="gemini-3.1-flash-lite", messages=[
        {"role": "user", "content": state.get("user_query") }
    ])
   
   state["llm_output"] = res.choices[0].message.content
   return state

def endnode(state: State):
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("evaluate_response", evaluate_response)
graph_builder.add_node("chatbot_gemini_lite", chatbot_gemini_lite)
graph_builder.add_node("endnode", endnode)


graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)

graph_builder.add_edge("chatbot_gemini_lite", "endnode")
graph_builder.add_edge("endnode",END)

graph = graph_builder.compile()
updated_state = graph.invoke(State({"user_query": "hey what is js?"}))
print(updated_state)