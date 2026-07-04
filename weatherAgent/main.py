from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

client = OpenAI(

    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
def get_weather(city):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    res = requests.get(url)
    if res.status_code == "200":
        return f"The weather in {city} is {res.text}"
    return f"something went wonrg"



def main():
    user_query = input("> ")
    res = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=[
            {'role': "user", 'content': user_query},
        ]
    )

    print(res.choices[0].message.content)


main()    