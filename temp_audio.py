import pynput
from pynput.keyboard import Key, Listener
charCount = 0
keys = []
def onKeyPress(key):
    try:
        print('Key Pressed : ',key)
        print(key)  #PrintK pressed key
        strKey =str(key)
        if strKey=="Key.media_play_pause":
            print("everything -------")
            exit(1)
    except Exception as ex:
        print('There was an error : ',ex)

with Listener(on_press=onKeyPress) as listener:
    listener.join()