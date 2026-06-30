from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(

    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

res = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[
        {'role': "user", 'content': "hey there"},
         {'role': "user", 'content': "i am kishan"}
    ]
)

print(res.choices[0].message.content)