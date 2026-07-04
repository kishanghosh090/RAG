from openai import OpenAI
from dotenv import load_dotenv
import requests
import subprocess
import re
from agent import SYSTEM_PROMT

load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def run_cmd(cmd: str):
    result = subprocess.run(cmd.split(" "))
    return result


def get_weather(city):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    res = requests.get(url)
    if res.status_code == 200:
        return f"The weather in {city} is {res.text}"
    return f"something went wrong"


available_tool = {
    "get_weather": get_weather,
    "run_cmd": run_cmd
}


def parse_tool_call(text):
    """Parse a tool call from the model's response text.

    Supported formats:
      - get_weather("malda")
      - get_weather(city="malda")
      - TOOL: get_weather("malda")
      - run_cmd("ls -la")
    """
    # Try to match tool_name(arg1, arg2, ...) or tool_name(key="val", ...)
    pattern = r"(?:TOOL:\s*)?(get_weather|run_cmd)\(([^)]*)\)"
    match = re.search(pattern, text)
    if not match:
        return None, None, None

    tool_name = match.group(1)
    args_str = match.group(2).strip()

    args = []
    kwargs = {}

    if args_str:
        # Split by commas that are NOT inside quotes
        parts = [p.strip() for p in re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', args_str)]
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if "=" in part:
                key, value = part.split("=", 1)
                kwargs[key.strip()] = value.strip().strip('"').strip("'")
            else:
                args.append(part.strip().strip('"').strip("'"))

    return tool_name, args, kwargs


def main():
    messages = [
        {"role": "system", "content": SYSTEM_PROMT}
    ]

    user_query = input("> ")
    messages.append({"role": "user", "content": user_query})

    max_iterations = 5

    for iteration in range(max_iterations):
        res = client.chat.completions.create(
            model="gemini-3.1-flash-lite",
            messages=messages,
        )

        response_text = res.choices[0].message.content
        print(f"\n[{iteration}] {response_text}\n")

        # Check if the response contains a tool call
        tool_name, args, kwargs = parse_tool_call(response_text)

        if tool_name and tool_name in available_tool:
            tool_func = available_tool[tool_name]
            try:
                if kwargs:
                    result = tool_func(**kwargs)
                elif args:
                    result = tool_func(*args)
                else:
                    result = tool_func()
            except Exception as e:
                result = f"Error executing {tool_name}: {e}"

            # Feed the tool result back to the model
            messages.append({"role": "assistant", "content": response_text})
            messages.append({"role": "user", "content": f"Tool result: {result}\n\nBased on the tool result, provide the final answer to the user's original query."})
        else:
            # No tool call → this is the final answer
            print("Final answer:", response_text)
            break


if __name__ == "__main__":
    main()