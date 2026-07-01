from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(

    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

res = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[
        {'role': "user", 'content': "hello you only releted to answer about programming nothing else"},
         {'role': "user", 'content': "i am kishan. 2 + 2??"}
    ]
)

print(res.choices[0].message.content)