from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()
client = Client(
    host="http://3.108.182.182:11434"
)

@app.get("/")
def read_root():
    return {"msg":"hello form FASTAPI"}


@app.post("/chat")
def chat(
        message: str = Body(...,description="the message")
):
    response = client.chat(model="qwen2.5:0.5b", messages=[
        {"role": "user", "content": message}
    ])
    return response.message.content
