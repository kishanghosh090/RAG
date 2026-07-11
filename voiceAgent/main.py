import speech_recognition as sr
import asyncio
import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()  

API_KEY = os.environ.get("GOOGLE_API_KEY") or ""
client = OpenAI(api_key=API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
async_client = AsyncOpenAI(api_key=API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

async def tts(text: str):
    async with async_client.audio.with_streaming_response.create(
        model="gemini-3.5-flash",
        voice="alloy",
        input=text,
        response_format="pcm"
    ) as response:
        async with LocalAudioPlayer(response) as player:
            await player.play()
            await response.stream_to(player)

async def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2
        print("Please say something...")
        audio = r.listen(source)

        print("Processing Audio...")

        stt = r.recognize_houndify(audio)

        print("You said: " + stt)

        SYSTEM_PROMPT = """You are a helpful assistant. you are a voice agent that can answer questions and provide information based on the user's input. Please respond in a clear and concise manner.
        you need to output as if you are a voice agent, and you need to provide information based on the user's input. You should not ask the user for more information, and you should not provide any personal opinions or advice. You should only provide factual information based on the user's input.
        """

        client_res = client.chat.completions.create(
            model="gemini-3.1-flash-lite",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": stt}
            ]
        )

        print("Assistant: " + client_res.choices[0].message.content)
        asyncio.run(tts(client_res.choices[0].message.content))


if __name__ == "__main__":
    asyncio.run(main())