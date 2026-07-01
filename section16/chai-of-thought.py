from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(

    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
# directly giving the inst to model
SYSTEM_PROMPT = """
    Your are an expert AI assistent reloving user quiries using chai of thought
    you work on START, PLAN and OUTPUT
    you need to first plan what need to be done. the PLAN can be multiple steps.
    once you think enough PLAN has been fone, finally you can give an OUTPUT


    RULES:
    - structly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START ( where user gives an input) PLAN(the can be multiple times) and finally OUTPUT .

    Output JSON format:
    {
        "step: "START" | "PLAN" | "OUTPUT",
        "content: "string"
    }

    Example:
    START: Hey, Can you solve 2 + 2 * 5 / 10
    PLAN: 
    {
        "step" : "PLAN",
        "content": "seems like user is interested in math"
    }

"""

res = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[
        {'role': "user", 'content': SYSTEM_PROMPT},
         {'role': "user", 'content': "tell me a joke"}
    ]
)

print(res.choices[0].message.content)