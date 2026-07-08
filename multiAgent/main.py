from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

res = client.chat.completions.create(
    model="gemini-3.1-flash-lite", # Check Google AI docs for model name
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "who is this person? i already know the name can you tell me more about him? and i know his github profile and linkedin profile. can you tell me more about him based on his github and linkedin profile?..is he a good software engineer? can you tell me about his skills and experience?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://avatars.githubusercontent.com/u/129781766"
                    }
                }
            ]
        }
    ]
)

print(res.choices[0].message.content)