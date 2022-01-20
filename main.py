import clipboard
import json
import time
from pynput import keyboard
import os.path

CB_FILEPATH = 'clipboard.json'
HOTKEY = '<ctrl>+c'
DATA = {}
COUNT = 0
CURRENT_DATETIME = time.asctime(time.localtime())


def on_activate():
    global DATA

    DATA = clipboard.paste()
    save_clipboard(DATA)
    pass


def for_canonical(f):
    return lambda k: f(listener.canonical(k))


def save_clipboard(data):
    with open(CB_FILEPATH, 'w') as file:
        json.dump(data, file, indent=4)


#def save_buffer(data):
    #time.sleep(60)
    #save_clipboard(data)


def pre_checks():
    fileExists = os.path.exists(CB_FILEPATH)
    global COUNT

    # Check if the file exists, if not, create it
    if not fileExists:
        with open(CB_FILEPATH, 'w') as file:
            json.dump({}, file)

    fileSize = os.path.getsize(CB_FILEPATH)
    # Resume the count from the last key if possible
    with open(CB_FILEPATH, 'r') as file:
        tempData = json.load(file)
        # Check if file is empty
        if not fileSize <= 2:
            getCount = list(tempData.keys())[-1]
            COUNT = getCount


pre_checks()
print(COUNT)

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse(HOTKEY),
    on_activate)

with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as listener:
    listener.join()
