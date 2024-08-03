import base64
import sys
import requests
import pyautogui
from openai import OpenAI
from pydub import AudioSegment
import io
from pynput.keyboard import Listener
from pygame import mixer
# r = sr.Recognizer()
# mic = sr.Microphone(device_index=3)
# api_key = "********************"

image_path = "/Users/raushanrkm/Desktop/workspace/ged/test.png"
speech_file_path = "/Users/raushanrkm/Desktop/workspace/ged/test.mp3"

eligible_to_play = False
mixer.init()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}



def onKeyPress(key):
    global eligible_to_play
    try:
        strKey = str(key)
        if len(sys.argv) > 1:
            print(sys.argv[1])
            text = sys.argv[1]
            text = text.replace("#", "") if text.startswith(
                "#") else f"This is software engineering interview question. please draw system diagram of {text} with explanation "
            # todo without image
            sys.argv.clear()
        if strKey == "Key.media_play_pause":
            text = "This is software engineering interview question. solve this question"
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
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def audio_trans(text):
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    return response.content

def startMicLoop(text):
    global eligible_to_play
    # with mic as source:
    #     r.adjust_for_ambient_noise(source)
    # continuously listen for input until interrupted

    # while True:

    # with mic as source:
    #     audio = r.listen(source, phrase_time_limit=10)
    # resText=''

    try:
        # use Google Speech Recognition to transcribe audio
        # process = multiprocessing. Process (target=audio_to_text, args=(audio, queue) )
        # text = r.recognize_google(audio, language='en-US')
        # print("You said:", text)
        # # check if sentence is complete by looking for punctuation marks
        # if text.endswith('.') or text.endswith('?') or text.endswith(' !'):
        #     print("Sentence complete.")
        # if 'stop' in text:
        #     for process in all_processes:
        #         process.terminate()
        #     continue;

        screenshot = pyautogui.screenshot()
        screenshot.save(image_path)
        base64_image = encode_image(image_path)
        resText = gpt4o_model(text, base64_image)
        file = '/Users/raushanrkm/Desktop/workspace/ged/test.txt'
        with open(file, 'w') as file_over_write:
                file_over_write.write(resText)
        tts_audio = audio_trans(resText)
        audio = AudioSegment.from_file(io.BytesIO(tts_audio), format="mp3")
        audio.export(speech_file_path, format='mp3')
        eligible_to_play = True

        # play _audio (audio) i
        # if not all_processes:
        #     process = multiprocessing.Process(target=play_audio)
        #     process.start()
        #     all_processes.append(process)
        # else:
        #     for process in all_processes:
        #         process.terminate()
        #         process = multiprocessing.Process(target=play_audio)
        #         process.start()
        #         all_processes.append(process)

    # except sr.UnknownValueError:
    #     a = 8
    # except sr.RequestError:
    #     print("Sorry, could not request results from the service.")
    except Exception as e:
        print(e)
        print("---restart again")

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
    print(resText)
    return resText


# # @app.get('/', response_class=HTMLResponse)
# def main(request: Request):
#     process = multiprocessing.Process(target=startMicLoop)
#     process.start()
#     return templates.TemplateResponse('index.html', {'request': request})


# @app.get("'/output")
# def output(request: Request):
    # screenshot = pyautogui.screenshot()
    # screenshot.save(image_path)
    # base64_image = encode_image(image_path)
    # time.sleep(1)
    # userText=queue.get ()
    # print (userText)
    # resText=gpt4o model (userText, base64_image)
    # tts_audio=audio_trans (resText)
    # audio = Audiosegment.from_file lio.BytesIO(tts_audio), format="mp3")
    # process = multiprocessing. Process (target-play audio, args=(audio, queue) )
    # process.start ()
    # thread = Thread ( target=play_audio, args=(audio, queue) )
    # all_processes. append (process)
    # play (audio)
    # return "success"

    # Function to encode the image


with Listener(on_press=onKeyPress) as listener:
    listener.join()