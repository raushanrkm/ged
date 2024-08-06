from time import sleep

from openai import OpenAI
import speech_recognition as sr
import json

r = sr.Recognizer()
mic = sr.Microphone(device_index=2)
client = OpenAI(api_key=api_key)


def startMicLoop():
    global question
    question = None
    try:
        if is_silent("audio_file.wav"):
            return
        audio_file = open("audio_file.wav", "rb")
        translation = client.audio.translations.create(model="whisper-1", file=audio_file)
        question = translation.text.lower()
        if len(question) < 5 or "thank" in question or "bye" in question or "okay" in question or "yeah" in question or "yep" in question or ". ." in question:
            question = None
        else:
            print(question)
            ask_question(question)
            question = None
    except Exception as e:
        question = None
    print("done")

def ask_question(question):
    if len(question) < 5:
        return
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f" this is software engineering question {question} ? please answer in short with few bullet points only",
            }
        ],
        model="gpt-3.5-turbo",
    )

    final_dictionary = json.loads(chat_completion.json())
    # print(final_dictionary)
    resText = final_dictionary["choices"][0]["message"]["content"]
    print("*************************************************************************************************")
    print(resText)
    print("*************************************************************************************************")
    print("done")

def is_silent(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        # Attempt to recognize any speech in the audio
        recognizer.recognize_google(audio)
        return False  # If no exception, audio is not silent
    except sr.UnknownValueError:
        return True  # If speech is unintelligible, consider it silent
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None  # Indicate an error occurred


with mic as source:
    r.adjust_for_ambient_noise(source)

while True:
    with mic as source:
        audio = r.listen(source, timeout=20, phrase_time_limit=6)
        with open("audio_file.wav", "wb") as file:
            file.write(audio.get_wav_data())
    # x = input("Already Speak")
    startMicLoop()
