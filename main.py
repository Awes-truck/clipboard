import clipboard
import sqlite3 as sql
import time
from pynput import keyboard
import os

HOTKEY = '<ctrl>+c'
CURRENT_DATETIME = time.asctime(time.localtime())
DB_PATH = 'clipboard.db'
PATH_DIR = os.path.abspath('clipboard.db')

conn = sql.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS clipboard (id INTEGER PRIMARY KEY, content TEXT NOT NULL, datetime TEXT NOT NULL)")
getTable = cursor.execute(
  """SELECT name FROM sqlite_master WHERE type='table'
  AND name='clipboard'; """).fetchall()
if getTable != []:
    conn.commit()
conn.close()


def on_activate():
    data = clipboard.paste()
    save_clipboard(data)


def for_canonical(f):
    return lambda k: f(listener.canonical(k))


def save_clipboard(data):
    global CURRENT_DATETIME
    conn = sql.connect(DB_PATH)
    insert = conn.cursor()
    insert.execute("INSERT INTO clipboard (content, datetime) VALUES (?, ?)",
                   (data, CURRENT_DATETIME))
    conn.commit()


def view_data():
    conn.close()
    view = sql.connect(DB_PATH)
    cursor = view.cursor()
    cursor.execute("SELECT * FROM clipboard")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


hotkey = keyboard.HotKey(
    keyboard.HotKey.parse(HOTKEY),
    on_activate)

with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as listener:
    listener.join()
