import base64
import sys

import openai
import requests
from fastapi.templating import Jinja2Templates
import pyautogui
from openai import OpenAI
from pydub import AudioSegment
import io
import speech_recognition as sr
from pynput.keyboard import Listener
from pygame import mixer
import json
import keyboard




# OpenAI API Key

freq = 44100
duration = 5
# app = FastAPI()
# templates = Jinja2Templates(directory='templates')
# all_processes = []
r = sr.Recognizer()
mic = sr.Microphone(device_index=2)
api_key = "**************"
client = OpenAI(api_key=api_key)


def startMicLoop():
    global question
    # global controlButton
    question = None
    with mic as source:
        r.adjust_for_ambient_noise(source)
    # continuously listen for input until interrupted
    print(" inside mic")
    try:
            with mic as source:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                with open("audio_file.wav", "wb") as file:
                    file.write(audio.get_wav_data())
            audio_file = open("audio_file.wav", "rb")
            translation = client.audio.translations.create(
                model="whisper-1",file=audio_file)
            question = translation.text.lower()
            if len(question) < 5 or "thank" in question or "bye" in question  or "okay" in question or "yeah" in question or "yep" in question or ". ." in question:
                question = 'a'
            else:
                print(question)
                ask_question(question)
                question ='a'
    except Exception as e:
            print(e)

def ask_question(question):
    if len(question) < 5:
        return
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f" this is software engineering question {question} ? please ans in short with few bullet points only",
            }
        ],
        model="gpt-3.5-turbo",
    )

    final_dictionary = json.loads(chat_completion.json())
    # print(final_dictionary)
    resText = final_dictionary["choices"][0]["message"]["content"]
    print(resText)
    print("done")


def onKeyPress(key):
    strKey = str(key)
    print(strKey)
    if strKey == "Key.shift_r":
        startMicLoop()
with Listener(on_press=onKeyPress) as listener:
    listener.join()