from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(

    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
# directly giving the inst to model
SYSTEM_PROMPT = "hello you only releted to answer about programming nothing else. Do not ans anyting else. your name is Alexa"

res = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[
        {'role': "user", 'content': SYSTEM_PROMPT},
         {'role': "user", 'content': "tell me a joke"}
    ]
)

print(res.choices[0].message.content)