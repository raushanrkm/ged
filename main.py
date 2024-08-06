import base64
import sys
import requests
import pyautogui
from openai import OpenAI
from pydub import AudioSegment
import io
from pynput.keyboard import Listener
from pygame import mixer

image_path = "/Users/raushanrkm/Desktop/workspace/ged/test.png"
speech_file_path = "/Users/raushanrkm/Desktop/workspace/ged/test.mp3"
text_output_file = '/Users/raushanrkm/Desktop/workspace/ged/test.txt'

eligible_to_play = False
mixer.init()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
client = OpenAI(api_key=api_key)



def onKeyPress(key):
    global eligible_to_play
    try:
        strKey = str(key)
        if len(sys.argv) > 1:
            print(sys.argv[1])
            text = sys.argv[1]
            text = text.replace("#", "") if text.startswith(
                "#") else f"This is software engineering interview question. please draw system diagram of {text} with explanation "
            ask_question(text)
            sys.argv.clear()
        if strKey == "Key.media_play_pause":
            text = "This is software engineering interview question. solve this question with explanation with most efficient time complexity and space complexit in java"
            startMicLoop(text)
        if eligible_to_play and strKey == "'a'":
            print("play")
            mixer.music.load(speech_file_path)
            mixer.music.set_volume(0.7)
            mixer.music.play()
        elif eligible_to_play and strKey == "'d'":
            print("resume")
            # Resuming the music
            mixer.music.unpause()
        elif eligible_to_play and strKey == "'f'":
            print("stop")
            # Stop the mixer
            mixer.music.stop()
            eligible_to_play = False
        elif eligible_to_play and strKey == "'s'":
            print("pause")
            # Stop the mixer
            mixer.music.pause()
        elif strKey == "'`'":
            exit(1)
    except Exception as ex:
        print('There was an error : ', ex)
        sys.argv.clear()
def encode_image(image_path):
    with open(image_path, "rb") as image_file:ssdds
        return base64.b64encode(image_file.read()).decode('utf-8')

def audio_trans(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    return response.content

def startMicLoop(text):
    global eligible_to_play
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(image_path)
        base64_image = encode_image(image_path)
        resText = gpt4o_model(text, base64_image)
        # with open(text_output_file, 'w') as file_over_write:
        #         file_over_write.write(resText)
        tts_audio = audio_trans(resText)
        print("done")

        audio = AudioSegment.from_file(io.BytesIO(tts_audio), format="mp3")
        audio.export(speech_file_path, format='mp3')
        eligible_to_play = True
    except Exception as e:
        print("click again")

def gpt4o_model(userText, base64_image):
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{userText}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4000
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    resJson = response.json()
    resText = resJson["choices"][0]["message"]["content"]
    print("*************************************************************************************************")
    print(resText)
    print("*************************************************************************************************")
    return resText
def ask_question(question):
    if len(question) < 5:
        return
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f" this is software engineering question {question} ? please answer in short with few "
                           f"bullet points only",
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



with Listener(on_press=onKeyPress) as listener:
    listener.join()