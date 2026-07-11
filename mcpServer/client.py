import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
# FIX 1: Import modern react agent from langgraph
from langgraph.prebuilt import create_react_agent

load_dotenv()

async def main():
    # Note: Ensure you are running this from the directory containing mathsserver.py
    client = MultiServerMCPClient({
        "math": {
            "command": "python",
            "args": ["mathsserver.py"], 
            "transport": "stdio"
        },
        "weather": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http"
        }
    })

    # Optional: ensure key is present
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
    
    # Connect and pull tools from the MCP server
    tools = await client.get_tools()
    
    # Initialize your model
    model = ChatGroq(model="qwen/qwen3-32b")
    
    # FIX 2: LangGraph's create_react_agent accepts model and tools directly
    agent = create_react_agent(
        model, 
        tools
    )

    # FIX 3: Changed .aivoke() to .ainvoke()
    weather_response = await agent.ainvoke(
        {
            "messages": [{
                "role": "user",
                "content": "what is weather in california?"
            }]
        }
    )

    # FIX 4: Fixed typo in list slicing ["messages"[-1]] -> ["messages"][-1]
    print("weather response: ", weather_response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
