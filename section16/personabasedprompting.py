from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(

    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


SYSTEM_PROMPT=""" 
    you are an AI persona assistant named kishan rana ghosh
    you are acting on behalf of piyush garg who is 20 year old tech enthusiast

"""


res = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[
        {'role': "user", 'content': SYSTEM_PROMPT},
         {'role': "user", 'content': "write a browser engine code in cpp"}
    ]
)
print(res.choices[0].message.content)