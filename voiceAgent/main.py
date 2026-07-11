import asyncio
import os
import tempfile

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from dotenv import load_dotenv
from gtts import gTTS
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

SYSTEM_PROMPT = """
You are a helpful voice assistant.

Respond naturally.
Keep answers concise (1-3 sentences).
Avoid markdown.
Avoid emojis.
"""


def speak(text: str):
    """Generate speech using gTTS and play it."""

    temp_file = None

    try:
        tts = gTTS(text=text, lang="en")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            temp_file = f.name

        tts.save(temp_file)

        data, samplerate = sf.read(temp_file, dtype="float32")

        print("----- Audio Info -----")
        print("Shape:", data.shape)
        print("Sample Rate:", samplerate)
        print("dtype:", data.dtype)
        print("----------------------")

        print(sd.query_devices(sd.default.device[1], "output"))

        sd.play(data, samplerate)
        sd.wait()

    except Exception as e:
        print("TTS Error:", e)

    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.pause_threshold = 0.8

        print("\n🎤 Speak...")

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10,
            )
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None

    print("Recognizing...")

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text

    except sr.UnknownValueError:
        print("Couldn't understand.")
        return None

    except sr.RequestError as e:
        print(e)
        return None


def ask_gemini(prompt: str):

    response = client.chat.completions.create(
model="gemini-2.5-flash",        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content.strip()


def main():

    while True:

        text = listen()

        if not text:
            continue

        if text.lower() in {
            "exit",
            "quit",
            "stop",
            "bye",
        }:
            print("Goodbye!")
            speak("Goodbye.")
            break

        reply = ask_gemini(text)

        print("\nAssistant:", reply)

        speak(reply)


if __name__ == "__main__":
    main()